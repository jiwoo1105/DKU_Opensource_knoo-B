import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import analysis_tool_result
import Boundary_logic as logic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm
import DB_request

# 한글 폰트 설정

# font_path = "C:\Users\LG\AppData\Local\Microsoft\Windows\Fonts\AppleSDGothicNeoM.ttf" # 글꼴 경로 설정
# font_name = fm.FontProperties(fname=font_path).get_name() # 폰트 이름 가져오기
# mpl.rc('font', family=font_name)
mpl.rcParams['font.family'] = 'malgun gothic'
mpl.rcParams['axes.unicode_minus'] = False

class MainView(QMainWindow):
    def __init__(self, user_emotion_result=None):
        super().__init__()
        self.user_emotion_result = user_emotion_result
        self.data_after_logic_book = None
        self.data_after_logic_movie = None
        
        # 차트 색상 설정
        self.colors = ['#FF8FA3', '#FFB3C1', '#FFC2D1', '#FFD1DC', '#FFE0E6', '#FFECF0', '#FFF0F5']
        self.setupUI()
        
        # 초기화 후 바로 결과 표시
        if self.user_emotion_result:
            self.show_result()

    def setupUI(self):
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_chart.ui"))
        UI_set.goto_result.clicked.connect(self.prepare_recommendations)  # 버튼 클릭 시 추천 준비 및 결과 창 열기

        # 차트를 표시할 Figure 생성
        self.figure = plt.Figure(facecolor='#FFFFFF')
        self.canvas = FigureCanvas(self.figure)
        
        # 기존 차트 위젯을 찾아서 레이아웃에 matplotlib 캔버스 추가
        chart_widget = UI_set.findChild(QWidget, "Show_result_by_chart")
        if chart_widget:
            layout = QVBoxLayout(chart_widget)
            layout.addWidget(self.canvas)

        self.setCentralWidget(UI_set)
        self.setWindowTitle("감정에 대한 분석 차트")
        self.resize(800, 600)  # 창 크기 키움
        self.show()

    #logic을 이용해서 감정 분석 결과를 후처리
    #각각 book과 movie의 db 조회에 가능한 감정 맵을 이용해서 감정끼리 매핑
    #감정 분석 결과를 필터링하고 바운더리 조정으로 data 정제
    #logic의 함수 이용
    def do_emo_logic_book(self):
        # 책 관련 감정 로직 처리
        self.data_after_logic_book = []  # 실제 로직 구현 필요
    
    def do_emo_logic_movie(self):
        # 영화 관련 감정 로직 처리
        self.data_after_logic_movie = []  # 실제 로직 구현 필요
    
    def show_result(self):
        # 감정 분석 결과를 문자열로 변환
        result_text = "감정 분석 결과:\n\n"  # 줄 간격 추가
        
        for emotion in self.user_emotion_result:
            # 백분율로 변환하여 표시
            percentage = emotion['score'] * 100
            result_text += f"{emotion['label']}: {percentage:.1f}%\n"
        
        # 사용자 감정 결과 텍스트 표시
        UI_set.Show_user_emotion.setText(result_text)
        
        # 차트 데이터 준비
        emotions = [emotion['label'] for emotion in self.user_emotion_result]
        values = [emotion['score'] for emotion in self.user_emotion_result]
        
        # 차트 그리기
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # 원형 차트 그리기
        wedges, texts, autotexts = ax.pie(values, 
                                        labels=emotions,
                                        colors=self.colors,
                                        autopct='%1.1f%%',
                                        startangle=90,
                                        pctdistance=0.85,
                                        wedgeprops=dict(width=0.5))  # 도넛 형태로 만들기
        
        # 차트 제목 설정
        ax.set_title('감정 분석 결과', pad=20, fontsize=16, fontweight='bold', fontfamily='malgun gothic', color='#FF8FA3')
        
        # 범례 설정
        ax.legend(wedges, emotions,
                title="감정",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                prop={'family': 'malgun gothic', 'color': '#FF8FA3', 'size': 10})
        
        # 텍스트 스타일 설정
        plt.setp(autotexts, size=9, weight="bold", fontfamily='malgun gothic', color='#FF8FA3')
        plt.setp(texts, size=11, fontfamily='malgun gothic', color='#FF8FA3')
        
        # 레이아웃 조정
        self.figure.tight_layout()
        
        # 차트 업데이트
        self.canvas.draw()

    def prepare_recommendations(self):
        # 감정 분석 결과를 튜플 리스트로 변환
        user_emotions = [(emotion['label'], emotion['score']) for emotion in self.user_emotion_result]
        
        # 책과 영화 추천 결과 가져오기
        self.data_after_logic_book = self.recom_book(user_emotions)
        self.data_after_logic_movie = self.recom_movie(user_emotions)
        
        # 결과 창 열기
        self.goto_result()

    def goto_result(self):
        # 사용자 감정을 튜플 리스트로 변환
        user_emotions = [(emotion['label'], emotion['score']) for emotion in self.user_emotion_result]
        self.S = analysis_tool_result.MainView(self.data_after_logic_book, self.data_after_logic_movie, user_emotions)

    def recom_book(self, user_emotions):
        # DB_request의 book_db 클래스 사용
        db = DB_request.book_db()
        return db.recom_book(user_emotions)  # user_emotions 인자 전달

    def recom_movie(self, user_emotions):
        # DB_request의 movie_db 클래스 사용
        db = DB_request.movie_db()
        return db.recom_movie(user_emotions)  # user_emotions 인자 전달

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    sys.exit(app.exec_())