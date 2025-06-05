import requests
import Boundary_logic as logic
import json
from datasets import load_dataset
import pandas as pd
import numpy as np
import os
#from analysis import emotion_analysis

#책 관련 DB 조회 클래스
#클래스 선언과 초기화후 사용 권장
#함수 직접 컨택 x
class book_db:

    global data # 추천/분석용 데이터
    global meta_data # 책 제목, 저자등의 메타데이터

    def __init__(self):
        self.load_data()

    def load_data(self):
        #허깅페이스에서 데이터셋 로드
        dataset = load_dataset("lime1327/book_data", data_dir="book_dataset")
        #metadata를 로컬에서 로드
        with open('book_metadata.json', encoding='utf-8') as f:
            meta = [json.loads(line) for line in f]

        self.data = pd.DataFrame(dataset['train'])
        self.meta_data = pd.DataFrame(meta)

    #구체성 값 계산 함수
    def normalized_tag_specificity(self,df):
        total_books = df['item_id'].nunique()
        tag_counts = df.groupby('tag')['item_id'].nunique()
        idf = np.log((total_books + 1) / (tag_counts + 1))
        min_val = idf.min()
        max_val = idf.max()
        norm_idf = (idf - min_val) / (max_val - min_val)
        return norm_idf
    

    #하나의 감정을 입력하면 그에 따른 결과를 출력
    #필요에 따라서 상위 n개의 결과로 제한
    def recommend_books_by_emotion(self, emotion, top_n = 100):
        # 감정 단어가 tag에 포함된 행만 필터링
        filtered = self.data[self.data['tag'].str.contains(emotion, case=False, na=False)]
        # 만약 평점 컬럼이 있으면, 높은 순으로 정렬
        if 'avg_rating' in filtered.columns:
            filtered = filtered.sort_values('avg_rating', ascending=False)
        # 상위 top_n개만 추출
        filtered = filtered.head(top_n)[['item_id', 'tag', 'avg_rating']]
        # 메타데이터(제목, 저자)와 병합
        result = filtered.merge(self.meta_data[['item_id', 'title', 'authors']], on='item_id', how='left')
        #중복되는 책 제거
        result = result[['title', 'authors', 'tag', 'avg_rating']].drop_duplicates(subset=['title', 'authors', 'tag'])
        result = result.head(top_n).reset_index(drop=True)  # 인덱스 재설정!

        # 정규화된 구체성 점수 붙이기
        norm_specificity = self.normalized_tag_specificity(self.data)
        result['norm_specificity'] = result['tag'].map(norm_specificity)
        #구체성 컬럼값 기준으로 내림차순 정렬
        #result = result.sort_values('norm_specificity', ascending=False).head(top_n).reset_index(drop=True)

        #top_n만 반환
        return result#.head(top_n)s
    
    #여러 감정들을 리스트로 받아서 전체 순회
    def lookup_all(self, text): 
        emotions = text # text => 유저의 감정 분석 결과 리스트 // 수치값을 빼고 어떤 태그가 있는지만 사용
        result = []
        for emo in emotions:
            recom = self.recommend_books_by_emotion(emo)
            result.extend(recom)
        return result

#db 조회 테스트용 코드
#db = book_db()
#print(db.recommend_books_by_emotion('funny'))

class movie_db:

    global dataset
    #global metadata

    def __init__(self):
        self.load_data()

    def load_data(self):
        #필요한 데이터 셋 직접 로드 // 현재는 3가지 데이터셋 로드중
        self.movies = load_dataset(
            "csv",
            data_files={
                "movies": "https://huggingface.co/datasets/lime1327/movie_data/resolve/main/archive/movie.csv"
            },
            split = "movies"
        )
        self.genome_tags = load_dataset(
            "csv",
            data_files={
                "genome_tags": "https://huggingface.co/datasets/lime1327/movie_data/resolve/main/archive/genome_tags.csv"
            },
            split = "genome_tags"
        )
        self.genome_scores = load_dataset(
            "csv",
            data_files={
                "genome_scores": "https://huggingface.co/datasets/lime1327/movie_data/resolve/main/archive/genome_scores.csv"
            },
            split = "genome_scores"
        )
  
    #emotion 입력을 통해 해당하는 태그로 db조회후 추천 영화를 받음
    def recommend_movies_by_emotion(self, emotion, top_n = 50):
        #데이터셋 변환
        movies = self.movies.to_pandas()
        genome_tags = self.genome_tags.to_pandas()
        genome_scores = self.genome_scores.to_pandas()

        #감정에 해당하는 태그 ID 찾기
        matched_tags = genome_tags[genome_tags['tag'].str.contains(emotion, case=False, na=False)]
        if matched_tags.empty:
            #입력한 태그와 일치하는 태그가 없다면.. -> 검색 불가 => 종료 or return -1 하고 따로 처리
            exit()

        # 여러 태그 중 relevance가 가장 높은 영화 추천 (상위 top_n개)
        recommendations = pd.DataFrame()

        for tag_id in matched_tags['tagId']:
            # 해당 태그의 relevance가 높은 영화 100개 추출
            tag_scores = genome_scores[genome_scores['tagId'] == tag_id]
            top_movies = tag_scores.sort_values(by='relevance', ascending=False).head(100)
            recommendations = pd.concat([recommendations, top_movies])

        #여러 태그가 있다면 relevance 높은 것 우선으로 정렬
        recommendations = recommendations.sort_values(by='relevance', ascending=False)

        #영화 정보와 조인
        recommendations = recommendations.merge(movies, on='movieId', how='left')
        recommendations = recommendations.drop_duplicates(subset='movieId')

        recom = recommendations[['title', 'relevance']].head(top_n).to_string(index=False)

        return recom
    
    def lookup_all(self, text):
        emotions = text # text => 유저의 감정 분석 결과 리스트 // 수치값을 빼고 어떤 태그가 있는지만 사용
        result = []
        for emo in emotions:
            recom = self.recommend_movies_by_emotion(emo)
            result.extend(recom)
        return result
    
    #입력되는 감정은 필터된 감정 or raw한 감정
    #raw한 감정의 경우 처리함수 불러서 내부에서 처리
    #필터된 감정은 그대로 사용
    #2가지 방안중 택 1
    def recom_movie(self):
        #movie_emotions.json 읽어서 DataFrame 생성
        with open("movie_emotions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        #각 영화별로 (title, emotion, score) 세 개 컬럼을 가진 DataFrame으로 전개
        rows = []
        for entry in data:
            title = entry["title"]
            for emotion, score in entry["emo_value"].items():
                rows.append({
                    "title": title,
                    "emotion": emotion,
                    "score": score
                })
        df = pd.DataFrame(rows)

        #테스트용 감정분석 셋 => 나중에 감정셋 따로 처리 에정
        user_emotions = [("불안", 0.7), ("행복", 0.4)]

        #감정별로 Top N개의 추천 결과 저장할 딕셔너리
        recommendations = {}

        for emotion, user_val in user_emotions:
            #해당 감정만 필터
            df_em = df[df["emotion"] == emotion].copy()
            #영화 점수와 사용자 값 차이 절댓값 계산
            df_em["diff"] = (df_em["score"] - user_val).abs()
            #diff 오름차순(작은 순) 정렬 후 상위 N개
            top10 = df_em.nsmallest(10, "diff")[["title", "score", "diff"]]
            #추천 결과 리스트에 저장
            #필요하다면 title만 뽑거나 score도 함께 보관할 수 있음
            recommendations[emotion] = top10

        #테스트 결과 출력 예시
        for emotion, rec_df in recommendations.items():
            print(f"\n=== 감정 '{emotion}' → 사용자 값: {dict(user_emotions)[emotion]} ===")
            print(rec_df.to_string(index=False))



#db 조회 테스트용 코드
db = movie_db()
db.recom_movie()
#rerom = db.recommend_movies_by_emotion('sad')
#print(rerom)




class music_db:
    #last.fm에서 받은 api발급 키와 name
    API_KEY    = '99d0ccd0deee6c19efcceb20c52b1a66'
    USER_AGENT = 'lime/1.0' # lime
    BASE_URL   = 'https://ws.audioscrobbler.com/2.0/'

    headers = {
        'user-agent': USER_AGENT
    }

    #임시 data // emo_list는 나중에 감정 처리된 값으로 받아올 예정
    emotion = 'happy'
    emo_list = ['happy','sad']

    #emo_list = logic.user_emo_logic()

    #단일 page 조회
    def lookup_page(self, emotion):
        tracks  = []
        params = {
            'method'  : 'tag.getTopTracks',
            'tag'     : emotion,
            'api_key' : self.API_KEY,
            'format'  : 'json',
            'limit'   : 50,
        }
        req = requests.get(self.BASE_URL, headers=self.headers, params=params)
        data = req.json()
        curr = data.get('tracks', {}).get('track', [])

        tracks.extend(curr)

        return tracks

    #emotion을 받아서 db 전체 순회
    #return 값은 list 형식
    # 매우 오래 걸림을 확인 -> 조정 필요
    def db_lookup_all(self,emotion):
        tracks = []
        page = 1

        #page 단위로 해당하는 emotion값에 따른 db 전체 조회
        while True:
            params = {
            'method'  : 'tag.getTopTracks',
            'tag'     : emotion,
            'api_key' : self.API_KEY,
            'format'  : 'json',
            'limit'   : 50,
            'page'    : page
            }
            
            req = requests.get(self.BASE_URL, headers=self.headers, params=params)
            data = req.json()

            curr = data.get('tracks', {}).get('track', [])

            if not curr:
                break

            tracks.extend(curr)
            page += 1

        return tracks

    #boundary를 이용해 처리된 감정들을 이용해서 각 감정들로 db 조회
    def lookup_for_all_emo(self,emo_list):
        curr = []
        for emo in emo_list:
            track = self.lookup_page(emo)
            for t in track:
                t['emotion'] = emo
            curr.extend(track)
        return curr

    #tracks = db_lookup_all(emotion)
    #tracks = lookup_for_all_emo(emo_list)
    #for t in tracks:
    #    print(f"[{t['emotion']}] {t['name']} — {t['artist']['name']}")



