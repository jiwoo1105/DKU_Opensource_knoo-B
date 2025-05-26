from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import sys
import os

# 상위 디렉토리 경로를 시스템 경로에 추가 (Boundary_logic 임포트를 위해)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Boundary_logic import print_boundary_results

def text_analy(user_input):
    # 모델 이름 지정
    model_name = "nlp04/korean_sentiment_analysis_dataset3_best"

    # 모델과 토크나이저 불러오기
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # 파이프라인 생성
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # 분석할 문장 입력
    text = user_input

    # 감정 분석 수행
    result = classifier(text)[0]

    # 감정 분석 (상위 7개 감정)
    results = classifier(text, top_k=7)

    # 결과 출력
    print("\n[감정 분석 결과]")
    for result in results:
        print(f"{result['label']}: {result['score']:.4f}")

    return results

if __name__ == "__main__":
    # 사용자 입력
    text = input("감정 분석할 문장을 입력하세요: ")
    
    # 감정 분석 수행
    results = text_analy(text)
    
    # 바운더리 분석 결과 출력
    print_boundary_results(results)