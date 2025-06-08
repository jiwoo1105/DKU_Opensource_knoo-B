"""
데이터베이스 요청 처리 모듈
책, 영화, 음악에 대한 감정 기반 추천 시스템을 구현한 클래스들을 포함
"""

import requests
import Boundary_logic as logic  # 감정 경계값 처리 로직
import json
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
import os

#from analysis import emotion_analysis

#책 관련 DB 조회 클래스
#클래스 선언과 초기화후 사용 권장
#함수 직접 컨택 x
class book_db:
    """
    책 추천 시스템을 위한 데이터베이스 클래스
    감정 기반으로 유사하거나 반대되는 책을 추천
    """

    global data  # 추천/분석용 데이터
    global meta_data  # 책 제목, 저자등의 메타데이터

    def recom_book(self, user_emotions, top_n = 10):
        """
        사용자의 감정을 기반으로 책을 추천하는 메서드
        
        Args:
            user_emotions: 사용자의 감정 상태 (감정-수치 쌍의 리스트)
            top_n: 추천할 책의 수 (기본값: 10)
            
        Returns:
            dict: 비슷한 감정('similar')과 반대 감정('opposite')의 책 추천 결과
        """
        #book_emotions.json 읽어서 DataFrame 생성
        with open("book_emotions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 사용자 감정을 딕셔너리로 변환
        user_emotion_dict = dict(user_emotions)
        
        # Boundary_logic을 사용하여 비슷한/반대되는 감정 추출
        similar_emotions = logic.similar_emo_logic(user_emotion_dict)
        opposite_emotions = logic.reverse_emo_logic(user_emotion_dict)
        
        # 각 책별로 전체 감정 유사도 계산 (비슷한 감정)
        similar_books = []
        opposite_books = []
        
        for book in data:
            title = book["title"]
            book_emotions = book["book_emotion"]
            
            # 비슷한 감정과의 유사도 계산
            similar_diff_squared = 0
            for emotion, user_val in similar_emotions.items():
                book_val = book_emotions.get(emotion, 0)
                diff = (user_val - book_val) ** 2
                similar_diff_squared += diff
            
            similar_similarity = (similar_diff_squared ** 0.5)
            similar_books.append({
                "title": title,
                "similarity": similar_similarity,
                "emotions": book_emotions
            })
            
            # 반대되는 감정과의 유사도 계산
            opposite_diff_squared = 0
            for emotion, user_val in opposite_emotions.items():
                book_val = book_emotions.get(emotion, 0)
                diff = (user_val - book_val) ** 2
                opposite_diff_squared += diff
            
            opposite_similarity = (opposite_diff_squared ** 0.5)
            opposite_books.append({
                "title": title,
                "similarity": opposite_similarity,
                "emotions": book_emotions
            })
        
        # 유사도 기준으로 정렬
        similar_books.sort(key=lambda x: x["similarity"])  # 유사도가 낮을수록 더 비슷
        opposite_books.sort(key=lambda x: x["similarity"])  # 반대 감정과 유사도가 낮을수록 더 반대
        
        return {
            "similar": similar_books[:top_n],
            "opposite": opposite_books[:top_n]
        }
    
    def search_and_get_book_summaries(self,text: str) -> List[Tuple[str, str]]:
        """
        OpenLibrary API를 사용해, 책 제목(title)에 `text`가 포함된 항목을 검색하고,
        각 항목의 제목과 줄거리(description)를 튜플로 묶어 리스트로 반환
        """
        results: List[Tuple[str, str]] = []

        #Search API 호출 (책 제목에 포함된 항목 검색)
        search_url = "https://openlibrary.org/search.json"
        params = {
            "title": text,   # 책 제목 필드에 text가 포함된 모든 항목 검색
            "limit": 10      # 필요에 따라 검색 결과 수량을 조절
        }

        try:
            resp = requests.get(search_url, params=params, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(f"[Error] OpenLibrary 검색 실패: {e}")
            return []

        data = resp.json()
        docs = data.get("docs", [])

        #검색 결과(docs) 순회
        for doc in docs:
            work_key = doc.get("key") 
            title    = doc.get("title")  # 책 제목

            if not work_key or not title:
                continue

            #/works/{work_key}.json 호출해서 description 필드 가져오기
            detail_url = f"https://openlibrary.org{work_key}.json"
            try:
                detail_resp = requests.get(detail_url, timeout=5)
                detail_resp.raise_for_status()
            except Exception as e:
                print(f"[Warning] 책 상세 정보 조회 실패: {work_key} → {e}")
                continue

            detail = detail_resp.json()
            desc = detail.get("description")

            # description이 dict인지 str인지 모두 처리
            if isinstance(desc, dict):
                summary = desc.get("value")
            elif isinstance(desc, str):
                summary = desc
            else:
                # 줄거리(description)가 없으면 건너뜀
                continue

            if not summary:
                continue

            #(책 제목, 줄거리) 튜플을 결과 목록에 추가
            results.append((title, summary))

        return results

#db 조회 테스트용 코드
"""
db = book_db()

text = "fun"
matches = db.search_and_get_book_summaries(text)

if not matches:
    print("검색 결과가 없거나 줄거리가 제공되지 않는 책입니다.")
else:
    print(f"\n'{text}'을(를) 포함한 책 중 줄거리가 있는 결과 {len(matches)}개:")
    for idx, (title, summary) in enumerate(matches, start=1):
        print(f"\n[{idx}] 제목: {title}\n줄거리:\n{summary}\n{'-'*40}")
"""



class movie_db:
    """
    영화 추천 시스템을 위한 데이터베이스 클래스
    감정 기반으로 유사하거나 반대되는 영화를 추천
    """

    global dataset
    #global metadata
    
    #입력되는 감정은 필터된 감정 or raw한 감정
    #raw한 감정의 경우 처리함수 불러서 내부에서 처리
    #필터된 감정은 그대로 사용
    #2가지 방안중 택 1
    def recom_movie(self, user_emotions):
        """
        사용자의 감정을 기반으로 영화를 추천하는 메서드
        
        Args:
            user_emotions: 사용자의 감정 상태 (감정-수치 쌍의 리스트)
            
        Returns:
            dict: 비슷한 감정('similar')과 반대 감정('opposite')의 영화 추천 결과 (각각 상위 10개)
        """
        #movie_emotions.json 읽어서 DataFrame 생성
        with open("movie_emotions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # 사용자 감정을 딕셔너리로 변환
        user_emotion_dict = dict(user_emotions)
        
        # Boundary_logic을 사용하여 비슷한/반대되는 감정 추출
        similar_emotions = logic.similar_emo_logic(user_emotion_dict)
        opposite_emotions = logic.reverse_emo_logic(user_emotion_dict)
        
        # 각 영화별로 전체 감정 유사도 계산 (비슷한 감정)
        similar_movies = []
        opposite_movies = []
        
        for movie in data:
            title = movie["title"]
            movie_emotions = movie["emo_value"]
            
            # 비슷한 감정과의 유사도 계산
            similar_diff_squared = 0
            for emotion, user_val in similar_emotions.items():
                movie_val = movie_emotions.get(emotion, 0)
                diff = (user_val - movie_val) ** 2
                similar_diff_squared += diff
            
            similar_similarity = (similar_diff_squared ** 0.5)
            similar_movies.append({
                "title": title,
                "similarity": similar_similarity,
                "emotions": movie_emotions
            })
            
            # 반대되는 감정과의 유사도 계산
            opposite_diff_squared = 0
            for emotion, user_val in opposite_emotions.items():
                movie_val = movie_emotions.get(emotion, 0)
                diff = (user_val - movie_val) ** 2
                opposite_diff_squared += diff
            
            opposite_similarity = (opposite_diff_squared ** 0.5)
            opposite_movies.append({
                "title": title,
                "similarity": opposite_similarity,
                "emotions": movie_emotions
            })
        
        # 유사도 기준으로 정렬
        similar_movies.sort(key=lambda x: x["similarity"])  # 유사도가 낮을수록 더 비슷
        opposite_movies.sort(key=lambda x: x["similarity"])  # 반대 감정과 유사도가 낮을수록 더 반대
        
        return {
            "similar": similar_movies[:10],
            "opposite": opposite_movies[:10]
        }
    
    def search_and_get_movie_summaries(self,text: str) -> List[Tuple[str, str, str]]:
        """
        TMDb API를 사용해, 영화 제목(title)에 `text`가 포함된 항목을 검색하고,
        각 영화의 (제목, 감독, 줄거리) 튜플을 리스트로 반환합니다.
        """

        #TMDb API 키 불러오기
        #제 개인 발급 키 입니다
        api_key = "b2fabf6e796b44bfd686fffdc21ddaf7"

        results: List[Tuple[str, str, str]] = []

        #검색 API 호출: /search/movie?api_key=...&query=<text>&language=ko-KR&page=1
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": api_key,
            "query": text,
            "language": "ko-KR",  # 한글 제목/줄거리 가져오려면 ko-KR, 영어면 en-US 로 변경
            "page": 1,
            "include_adult": False
        }

        try:
            resp = requests.get(search_url, params=params, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(f"[Error] TMDb 검색 실패: {e}")
            return []

        data = resp.json()
        movies = data.get("results", [])

        #검색된 각 영화마다 상세 정보 조회
        for movie in movies:
            movie_id = movie.get("id")
            title    = movie.get("title") or movie.get("original_title")
            overview = movie.get("overview")  # 이미 search 결과에 overview가 있지만, 상세 조회 시 업데이트될 수도 있음

            if not movie_id or not title:
                continue

            #상세 정보 + credits 조회: /movie/{movie_id}?api_key=...&language=ko-KR&append_to_response=credits
            detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            detail_params = {
                "api_key": api_key,
                "language": "ko-KR",
                "append_to_response": "credits"
            }

            try:
                detail_resp = requests.get(detail_url, params=detail_params, timeout=5)
                detail_resp.raise_for_status()
            except Exception as e:
                print(f"[Warning] 영화 상세 정보 조회 실패: ID={movie_id} → {e}")
                # search 결과의 overview라도 남기고, 감독을 "정보 없음"으로 둠
                director = "감독 정보 없음"
                summary  = overview or ""
                results.append((title, director, summary))
                continue

            detail = detail_resp.json()
            # 줄거리 (overview) 갱신
            summary = detail.get("overview") or ""

            #감독(director) 찾기: credits -> crew 중 job="Director"
            credits = detail.get("credits", {})
            crew_list = credits.get("crew", [])
            director: Optional[str] = None
            for member in crew_list:
                if member.get("job") == "Director":
                    director = member.get("name")
                    break
            if director is None:
                director = "감독 정보 없음"

            #(제목, 감독, 줄거리) 튜플로 결과에 추가
            results.append((title, director, summary))

        return results







