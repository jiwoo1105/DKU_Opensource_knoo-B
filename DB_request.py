import requests
import Boundary_logic as logic
import json
from datasets import load_dataset
import pandas as pd
from analysis import emotion_analysis

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

    #하나의 감정을 입력하면 그에 따른 결과를 출력
    #필요에 따라서 상위 n개의 결과로 제한
    def recommend_books_by_emotion(self, emotion, top_n = 10):
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

        #top_n만 반환
        return result.head(top_n)
    
    #여러 감정들을 리스트로 받아서 전체 순회
    def lookup_all(self, text):
        emotions = text # text => 유저의 감정 분석 결과 
        result = []
        for emo in emotions:
            recom = self.recommend_books_by_emotion(emo)
            result.extend(recom)
        return result


db = book_db()
print(db.recommend_books_by_emotion('adventure'))

class movie_db:
    a = 0


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



