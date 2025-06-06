"""
데이터베이스 요청 처리 모듈
책, 영화, 음악에 대한 감정 기반 추천 시스템을 구현한 클래스들을 포함
"""

import requests
import Boundary_logic as logic  # 감정 경계값 처리 로직
import json
import pandas as pd
import numpy as np
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

#db 조회 테스트용 코드
#db = book_db()
#db.recom_book([("불안", 0.7), ("행복", 0.4)])


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

#db 조회 테스트용 코드
#db = movie_db()
#db.recom_movie([("불안", 0.7), ("행복", 0.4)])
#rerom = db.recommend_movies_by_emotion('sad')
#print(rerom)



