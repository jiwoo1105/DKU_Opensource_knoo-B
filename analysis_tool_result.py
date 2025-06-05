import sys
import os
import DB_request as DB  # 데이터베이스 요청 처리 모듈
import Boundary_logic as logic  # 감정 경계 로직 처리 모듈
from analysis import emotion_analysis  # 감정 분석 모듈
from PySide2 import QtUiTools, QtGui  # Qt GUI 라이브러리
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout


class MainView(QMainWindow):
    """
    추천 결과를 보여주는 메인 윈도우 클래스
    책과 영화 추천 결과를 UI에 표시
    """
    #책과 관련된 정리된 데이터
    global data_after_logic_book
    global data_after_logic_movie
 
    def __init__(self, book_recommendations=None, movie_recommendations=None):
        """
        메인 윈도우 초기화
        Args:
            book_recommendations: 책 추천 결과 데이터
            movie_recommendations: 영화 추천 결과 데이터
        """
        super().__init__()
        self.book_recommendations = book_recommendations
        self.movie_recommendations = movie_recommendations
        self.setupUI()

    def setupUI(self):
        """
        UI 구성요소 초기화 및 설정
        - UI 파일 로드
        - 결과 표시
        - 윈도우 설정
        """
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_result.ui"))
        self.show_result()
        self.setCentralWidget(UI_set)
        self.setWindowTitle("추천 결과")
        self.resize(510, 350)
        self.show()

    def show_result(self):
        """
        책과 영화 추천 결과를 UI에 표시하는 메서드
        - 비슷한 감정의 콘텐츠 추천 결과 표시
        - 반대 감정의 콘텐츠 추천 결과 표시
        - 각 항목별 감정 분포도 표시
        """
        book_text = ""
        movie_text = ""

        if self.book_recommendations:
            # 비슷한 감정의 책 추천 결과 처리
            book_text += "비슷한 감정의 책 추천:\n"
            for book in self.book_recommendations["similar"]:
                book_text += f"- {book['title']} (유사도: {book['similarity']:.3f})\n"
                book_text += "  감정 분포:\n"
                for emotion, score in book['emotions'].items():
                    book_text += f"    {emotion}: {score:.3f}\n"
                book_text += "\n"
            
            # 반대 감정의 책 추천 결과 처리
            book_text += "\n반대 감정의 책 추천:\n"
            for book in self.book_recommendations["opposite"]:
                book_text += f"- {book['title']} (유사도: {book['similarity']:.3f})\n"
                book_text += "  감정 분포:\n"
                for emotion, score in book['emotions'].items():
                    book_text += f"    {emotion}: {score:.3f}\n"
                book_text += "\n"
        else:
            book_text = "추천할 수 있는 책이 없습니다."

        if self.movie_recommendations:
            # 비슷한 감정의 영화 추천 결과 처리
            movie_text += "비슷한 감정의 영화 추천:\n"
            for movie in self.movie_recommendations["similar"]:
                movie_text += f"- {movie['title']} (유사도: {movie['similarity']:.3f})\n"
                movie_text += "  감정 분포:\n"
                for emotion, score in movie['emotions'].items():
                    movie_text += f"    {emotion}: {score:.3f}\n"
                movie_text += "\n"
            
            # 반대 감정의 영화 추천 결과 처리
            movie_text += "\n반대 감정의 영화 추천:\n"
            for movie in self.movie_recommendations["opposite"]:
                movie_text += f"- {movie['title']} (유사도: {movie['similarity']:.3f})\n"
                movie_text += "  감정 분포:\n"
                for emotion, score in movie['emotions'].items():
                    movie_text += f"    {emotion}: {score:.3f}\n"
                movie_text += "\n"
        else:
            movie_text = "추천할 수 있는 영화가 없습니다."

        # UI에 결과 텍스트 설정
        UI_set.recommend_book.setText(book_text)
        UI_set.recommend_movie.setText(movie_text)

    def goto_first(self):
        """
        초기 화면으로 돌아가는 함수 (추후 구현 예정)
        Returns:
            0: 임시 반환값
        """
        return 0
    
    def do_emo_logic(self):
        """
        사용자 감정에 대한 로직 처리를 수행하는 메서드
        - 비슷한 감정과 반대 감정에 대한 로직 처리
        - 처리된 결과를 data_after_logic_book에 저장
        """
        self.data_after_logic_book = [] 
        # 책 관련 감정 로직 처리
        similar_data = logic.similar_emo_logic(self.user_emotion_result)
        reverse_data = logic.reverse_emo_logic(self.user_emotion_result)
        self.data_after_logic_book.append(similar_data)
        self.data_after_logic_book.append(reverse_data)
    
    def get_recom_book(self):
        """
        책 추천 결과를 가져오는 메서드 (현재 미구현)
        Returns:
            list: 빈 결과 리스트
        """
        result  = []
        db = DB.book_db()
        # data => logic을 이용해 정제된 data
        data = self.user_emotion_result
        return result

    def get_recom_movie(self):
        """
        영화 추천 결과를 가져오는 메서드
        Returns:
            list: 추천된 영화 목록
        """
        result = []
        db = DB.movie_db()
        for emo in self.data_after_logic_book:
            value = 1  # emo에서 수치값 컬럼을 받아오는 변수
            result.append(db.recom_movie(emo))
        return result

def resource_path(relative_path):
    """
    리소스 파일의 절대 경로를 반환하는 헬퍼 함수
    PyInstaller로 실행 파일 생성 시 필요
    
    Args:
        relative_path: 상대 경로
    Returns:
        str: 절대 경로
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Qt 애플리케이션 생성
    main = MainView()  # 메인 윈도우 생성
    sys.exit(app.exec_())  # 이벤트 루프 시작
