import requests
import Boundary_logic as logic
import json
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

    def recom_book(self,top_n = 10):
        #book_emotions.json 읽어서 DataFrame 생성
        with open("book_emotions.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        rows = []
        for entry in data:
            title = entry["title"]
            for emotion, score in entry["book_emotion"].items():
                rows.append({
                    "title": title,
                    "emotion": emotion,
                    "score": score
                })

        df = pd.DataFrame(rows)
        # 사용자 감정 리스트 A (예시)
        user_emotions = [("불안", 0.7), ("행복", 0.4)]

        # 감정별로 Top 10 가장 근접한 책을 찾는 로직
        recommendations = {}

        for emotion, user_val in user_emotions:
            #해당 감정만 필터
            df_em = df[df["emotion"] == emotion].copy()
            
            #절댓값 차이(diff) 계산
            df_em["diff"] = (df_em["score"] - user_val).abs()
            
            # diff 오름차순 정렬 후 상위 10개
            top10 = df_em.nsmallest(top_n, "diff")[["title", "score", "diff"]]
            
            #추천 결과 저장
            recommendations[emotion] = top10

        # 결과 출력 test
        for emotion, rec_df in recommendations.items():
            print(f"\n=== 감정 '{emotion}' → 사용자 값: {dict(user_emotions)[emotion]} ===")
            print(rec_df.to_string(index=False))

        return recommendations

#db 조회 테스트용 코드
db = book_db()
db.recom_book()


class movie_db:

    global dataset
    #global metadata
    
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



