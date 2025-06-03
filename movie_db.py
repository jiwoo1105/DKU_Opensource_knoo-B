import os
import sys
import json
import time
import requests
import pandas as pd
from typing import Optional, List, Dict

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm


#------------------------------------------------------------------------------
# 1) 감정 분석 함수(text_analy) 리팩터링: Token 길이 체크 후 청크 단위 처리
#------------------------------------------------------------------------------
class SentimentAnalyzer:
    """
    transformers pipeline("text-classification")을 한 번만 초기화하고,
    입력 텍스트가 512 토큰을 넘으면 자동으로 청크(512 토큰씩)로 나눠 분석 후
    라벨별 점수를 평균 내서 반환합니다.
    """
    def __init__(self, model_name: str = "nlp04/korean_sentiment_analysis_dataset3_best", chunk_size: int = 512):
        # 1) 토크나이저 + 모델을 한 번만 로드
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model     = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.classifier = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            return_all_scores=False
        )
        self.chunk_size = chunk_size

    def analyze(self, text: str, top_k: int = 7) -> Dict[str, float]:
        """
        text를 토크나이즈해서 토큰 길이가 chunk_size(512)를 넘으면
        여러 청크로 나눠 각각 감정 분석을 수행한 뒤, 라벨별 점수를 평균 내서 반환합니다.

        반환 형식: { "Joy": 0.7123, "Sadness": 0.0543, … }
        """
        # 전체 텍스트를 토크나이즈(토큰 ID 리스트) — truncation=False로 원본 길이 유지
        encoding = self.tokenizer(text, return_tensors="pt", truncation=False, padding=False)
        input_ids = encoding["input_ids"][0]  # shape: [총_토큰_길이]

        # 토큰 길이가 chunk_size 이하라면, pipeline을 한 번만 호출
        if len(input_ids) <= self.chunk_size:
            results = self.classifier(
                text,
                top_k=top_k,
                truncation=True,       # 혹시 텍스트가 미세하게 over되더라도 잘라줌
                max_length=self.chunk_size
            )
            # results 예: [ {"label":"Joy","score":0.70}, … ] (최대 top_k 개)
            return { r["label"]: float(r["score"]) for r in results }

        # chunk_size를 초과하는 경우: 청크 단위로 나눠서 분석
        chunk_dicts: List[Dict[str, float]] = []
        for i in range(0, len(input_ids), self.chunk_size):
            chunk_ids = input_ids[i : i + self.chunk_size]
            # 청크 토큰 ID를 다시 텍스트로 디코드
            chunk_text = self.tokenizer.decode(
                chunk_ids,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            # 청크별 감정 분석
            chunk_results = self.classifier(
                chunk_text,
                top_k=top_k,
                truncation=True,
                max_length=self.chunk_size
            )
            # chunk_results 예: [ {"label":"Joy","score":0.55}, … ]
            chunk_dicts.append({ r["label"]: float(r["score"]) for r in chunk_results })

        # 모든 청크에서 등장한 라벨들을 모아서 '전체 라벨 세트' 추출
        all_labels = set()
        for d in chunk_dicts:
            all_labels.update(d.keys())

        # 라벨별로 모든 청크의 점수를 합산(없으면 0)한 뒤, 청크 개수로 나눠 평균 계산
        num_chunks = len(chunk_dicts)
        averaged: Dict[str, float] = {}
        for lbl in all_labels:
            total_score = sum(d.get(lbl, 0.0) for d in chunk_dicts)
            averaged[lbl] = total_score / num_chunks

        return averaged


#------------------------------------------------------------------------------
# 2) Open Library API 헬퍼 클래스 (변경 없음)
#------------------------------------------------------------------------------
class OpenLibraryClient:
    SEARCH_URL = "https://openlibrary.org/search.json"
    WORKS_URL  = "https://openlibrary.org{work_key}.json"
    TIMEOUT    = 5

    @staticmethod
    def get_description(title: str, author: Optional[str] = None) -> Optional[str]:
        """
        책 제목(title) (옵션: author) 으로 OpenLibrary에 검색 → 첫 번째 결과 work_key 추출
        → /works/{work_key}.json 호출 후 description(줄거리) 반환. 실패 시 None.
        """
        params = {"title": title}
        if author:
            params["author"] = author

        try:
            resp = requests.get(OpenLibraryClient.SEARCH_URL, params=params, timeout=OpenLibraryClient.TIMEOUT)
            data = resp.json()
        except Exception as e:
            print(f"[Warning] OpenLibrary 검색 실패: '{title}' → {e}")
            return None

        docs = data.get("docs", [])
        if not docs:
            return None

        work_key = docs[0].get("key")  # ex: "/works/OL12345W"
        if not work_key:
            return None

        try:
            detail = requests.get(
                OpenLibraryClient.WORKS_URL.format(work_key=work_key),
                timeout=OpenLibraryClient.TIMEOUT
            ).json()
        except Exception as e:
            print(f"[Warning] OpenLibrary 상세 정보 실패: '{title}' → {e}")
            return None

        desc = detail.get("description")
        if desc is None:
            return None
        if isinstance(desc, dict):
            return desc.get("value")
        elif isinstance(desc, str):
            return desc
        else:
            return None

def main():
    csv_path = os.path.join(os.path.dirname(__file__), "movies.csv")
    df = pd.read_csv(
        csv_path,
        usecols=["movieId", "title"],
        dtype={"movieId": int, "title": str},
        quoting=1  # csv.QUOTE_ALL
    )
    titles = df["title"].tolist()

    # SentimentAnalyzer 한 번만 초기화
    analyzer = SentimentAnalyzer()

    output_list: List[Dict] = []

    for title in tqdm(titles, desc="Processing titles"):
        # Open Library에서 줄거리(description) 가져오기
        plot = OpenLibraryClient.get_description(title)
        if not plot:
            # 줄거리 없으면 건너뛰기
            continue

        # sentiment 분석 (chunk 처리 포함)
        emo_dict = analyzer.analyze(plot, top_k=7)
        # emo_dict 예: { "Joy": 0.65, "Sadness": 0.10, ... }

        # 결과 누적
        output_list.append({
            "title"    : title,
            "emo_value": emo_dict
        })

        # API 과부하 방지용 짧은 대기
        time.sleep(0.2)

    # JSON으로 저장
    out_path = os.path.join(os.path.dirname(__file__), "movie_emotions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 완료: {len(output_list)}개 항목이 '{out_path}'에 저장되었습니다.")


if __name__ == '__main__':
    main()

