import sys
import os
import DB_request as DB  # 데이터베이스 요청 처리 모듈
import Boundary_logic as logic  # 감정 경계 로직 처리 모듈
from analysis import emotion_analysis  # 감정 분석 모듈
from PySide2 import QtUiTools, QtGui  # Qt GUI 라이브러리
from PySide2.QtWidgets import (QMainWindow, QApplication, QFileDialog, QWidget, 
                             QLabel, QVBoxLayout, QPushButton, QTextBrowser,
                             QTabWidget, QScrollArea, QHBoxLayout, QFrame)
from PySide2.QtCore import Qt


class MainView(QMainWindow):
    """
    추천 결과를 보여주는 메인 윈도우 클래스
    책과 영화 추천 결과를 UI에 표시
    """
    #책과 관련된 정리된 데이터
    global data_after_logic_book
    global data_after_logic_movie
 
    def __init__(self, book_recommendations=None, movie_recommendations=None, user_emotions=None):
        """
        메인 윈도우 초기화
        Args:
            book_recommendations: 책 추천 결과 데이터
            movie_recommendations: 영화 추천 결과 데이터
            user_emotions: 사용자 감정 분석 결과
        """
        super().__init__()
        self.book_recommendations = book_recommendations
        self.movie_recommendations = movie_recommendations
        self.user_emotions = user_emotions  # DB_request에서 전달받은 사용자 감정
        self.setupUI()

    def create_emotion_display(self, emotions, title="감정 분포"):
        """감정 분포를 보여주는 위젯을 생성합니다."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 제목 레이블
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #FF8FA3;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background-color: #FFF0F5;
                border-radius: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        # 감정 분포 표시
        emotion_text = QTextBrowser()
        emotion_text.setMaximumHeight(200)
        emotion_text.setStyleSheet("""
            QTextBrowser {
                border: 2px solid #FFE4E1;
                border-radius: 10px;
                background-color: #FFFFFF;
                padding: 15px;
                font-size: 12px;
                line-height: 1.6;
                color: #FF8FA3;
            }
        """)
        
        emotion_text_content = ""
        if isinstance(emotions, dict):
            sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
            for emotion, score in sorted_emotions:
                emotion_text_content += f"{emotion}: {score:.4f}\n"
        elif isinstance(emotions, list):
            # DB_request 형식의 감정 데이터 처리 (튜플 리스트)
            if len(emotions) > 0 and isinstance(emotions[0], tuple):
                sorted_emotions = sorted(emotions, key=lambda x: x[1], reverse=True)
                for emotion, score in sorted_emotions:
                    emotion_text_content += f"{emotion}: {score:.4f}\n"
            else:
                sorted_emotions = sorted(emotions, key=lambda x: x['score'], reverse=True)
                for emotion in sorted_emotions:
                    emotion_text_content += f"{emotion['label']}: {emotion['score']:.4f}\n"
                
        emotion_text.setText(emotion_text_content)
        layout.addWidget(emotion_text)
        
        return widget

    def create_content_widget(self, title, similarity, emotions):
        """콘텐츠 항목을 위한 위젯을 생성합니다."""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        
        # 제목과 유사도를 표시하는 컨테이너
        title_container = QWidget()
        title_container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border: 2px solid #FFE4E1;
                border-radius: 15px;
                padding: 15px;
                margin: 5px;
            }
        """)
        title_layout = QVBoxLayout(title_container)
        
        # 제목 레이블
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            QLabel {
                color: #FF8FA3;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        title_layout.addWidget(title_label)
        
        # 유사도 레이블
        similarity_label = QLabel(f"감정 유사도: {similarity:.3f}")
        similarity_label.setStyleSheet("""
            QLabel {
                color: #FF8FA3;
                font-size: 12px;
                padding: 2px 5px;
                background-color: #FFF0F5;
                border-radius: 10px;
            }
        """)
        title_layout.addWidget(similarity_label)
        
        main_layout.addWidget(title_container)
        
        # 감정 분포 관련 위젯들을 담을 컨테이너
        emotions_container = QWidget()
        emotions_container.hide()  # 초기에는 숨김
        emotions_layout = QHBoxLayout(emotions_container)
        emotions_layout.setSpacing(20)  # 위젯 사이 간격 설정
        
        # 콘텐츠의 감정 분포
        content_emotions = self.create_emotion_display(emotions, "콘텐츠 감정 분포")
        emotions_layout.addWidget(content_emotions)
        
        # 구분선 추가
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("""
            background-color: #FFE4E1;
            margin: 0px 10px;
        """)
        emotions_layout.addWidget(line)
        
        # 사용자의 감정 분포
        if self.user_emotions:
            user_emotions = self.create_emotion_display(self.user_emotions, "사용자 감정 분포")
            emotions_layout.addWidget(user_emotions)
        
        main_layout.addWidget(emotions_container)
        
        # 감정 분포 토글 버튼
        emotion_btn = QPushButton("감정 분포 비교하기")
        emotion_btn.setCheckable(True)
        emotion_btn.setMaximumWidth(200)
        emotion_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFE4E1;
                color: #FF8FA3;
                border: none;
                padding: 10px 20px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FFD0CC;
            }
            QPushButton:checked {
                background-color: #FF8FA3;
                color: white;
            }
        """)
        main_layout.addWidget(emotion_btn)
        
        # 버튼 클릭 이벤트 연결
        emotion_btn.toggled.connect(emotions_container.setVisible)
        
        # 구분선 추가
        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.HLine)
        bottom_line.setStyleSheet("""
            background-color: #FFE4E1;
            margin: 15px 0px;
        """)
        main_layout.addWidget(bottom_line)
        
        return widget

    def setupUI(self):
        """
        UI 구성요소 초기화 및 설정
        - UI 파일 로드
        - 결과 표시
        - 윈도우 설정
        """
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_result.ui"))
        
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #FFF5F7;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #FFFFFF;
                color: #FF8FA3;
                padding: 10px 25px;
                border: 2px solid #FFE4E1;
                margin-right: 4px;
                border-radius: 15px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #FFE4E1;
                color: #FF8FA3;
                border: 2px solid #FFD0CC;
            }
            QTabBar::tab:hover {
                background: #FFF0F5;
                border: 2px solid #FFD0CC;
            }
        """)
        
        # 4개의 탭을 위한 스크롤 영역과 위젯 생성
        self.similar_book_scroll = QScrollArea()
        self.opposite_book_scroll = QScrollArea()
        self.similar_movie_scroll = QScrollArea()
        self.opposite_movie_scroll = QScrollArea()
        
        # 각 탭의 컨텐츠 위젯 생성
        self.similar_book_widget = QWidget()
        self.opposite_book_widget = QWidget()
        self.similar_movie_widget = QWidget()
        self.opposite_movie_widget = QWidget()
        
        # 각 위젯의 레이아웃 설정
        self.similar_book_layout = QVBoxLayout(self.similar_book_widget)
        self.opposite_book_layout = QVBoxLayout(self.opposite_book_widget)
        self.similar_movie_layout = QVBoxLayout(self.similar_movie_widget)
        self.opposite_movie_layout = QVBoxLayout(self.opposite_movie_widget)
        
        # 스크롤 영역 설정
        for scroll, widget in [
            (self.similar_book_scroll, self.similar_book_widget),
            (self.opposite_book_scroll, self.opposite_book_widget),
            (self.similar_movie_scroll, self.similar_movie_widget),
            (self.opposite_movie_scroll, self.opposite_movie_widget)
        ]:
            scroll.setWidget(widget)
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background: #FFF5F7;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #FFF0F5;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #FFE4E1;
                    min-height: 20px;
                    border-radius: 6px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            """)
        
        # 탭 추가
        self.tab_widget.addTab(self.similar_book_scroll, "비슷한 감정의 책 Top 10")
        self.tab_widget.addTab(self.opposite_book_scroll, "반대 감정의 책 Top 10")
        self.tab_widget.addTab(self.similar_movie_scroll, "비슷한 감정의 영화 Top 10")
        self.tab_widget.addTab(self.opposite_movie_scroll, "반대 감정의 영화 Top 10")
        
        # 기존 위젯을 탭 위젯으로 교체
        UI_set.verticalLayout.addWidget(self.tab_widget)
        
        self.show_result()
        self.setCentralWidget(UI_set)
        self.setWindowTitle("추천 결과")
        self.resize(1000, 600)  # 창 크기 키움
        self.show()

    def show_result(self):
        """
        책과 영화 추천 결과를 UI에 표시하는 메서드
        """
        if self.book_recommendations:
            # 비슷한 감정의 책 추천 결과 처리
            for book in self.book_recommendations["similar"]:
                widget = self.create_content_widget(book['title'], book['similarity'], book['emotions'])
                self.similar_book_layout.addWidget(widget)
            self.similar_book_layout.addStretch()
            
            # 반대 감정의 책 추천 결과 처리
            for book in self.book_recommendations["opposite"]:
                widget = self.create_content_widget(book['title'], book['similarity'], book['emotions'])
                self.opposite_book_layout.addWidget(widget)
            self.opposite_book_layout.addStretch()
        else:
            self.similar_book_layout.addWidget(QLabel("추천할 수 있는 책이 없습니다."))
            self.opposite_book_layout.addWidget(QLabel("추천할 수 있는 책이 없습니다."))

        if self.movie_recommendations:
            # 비슷한 감정의 영화 추천 결과 처리
            for movie in self.movie_recommendations["similar"]:
                widget = self.create_content_widget(movie['title'], movie['similarity'], movie['emotions'])
                self.similar_movie_layout.addWidget(widget)
            self.similar_movie_layout.addStretch()
            
            # 반대 감정의 영화 추천 결과 처리
            for movie in self.movie_recommendations["opposite"]:
                widget = self.create_content_widget(movie['title'], movie['similarity'], movie['emotions'])
                self.opposite_movie_layout.addWidget(widget)
            self.opposite_movie_layout.addStretch()
        else:
            self.similar_movie_layout.addWidget(QLabel("추천할 수 있는 영화가 없습니다."))
            self.opposite_movie_layout.addWidget(QLabel("추천할 수 있는 영화가 없습니다."))

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
