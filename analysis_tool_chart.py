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

# 한글 폰트 설정
mpl.rcParams['font.family'] = 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

class MainView(QMainWindow):
    def __init__(self, user_emotion_result=None):
        super().__init__()
        self.user_emotion_result = user_emotion_result
        self.data_after_logic_book = None
        self.data_after_logic_movie = None
        
        # 차트 색상 설정
        self.colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFB366']
        self.setupUI()
        
    def setupUI(self):
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_chart.ui"))
        UI_set.goto_result.clicked.connect(self.goto_result)

        # 차트를 표시할 Figure 생성
        self.figure = plt.Figure(facecolor='#F0F0F0')
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
        
        if self.user_emotion_result:
            self.show_result()

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
        ax.set_title('감정 분석 결과', pad=20, fontsize=14, fontweight='bold', fontfamily='AppleGothic')
        
        # 범례 설정
        ax.legend(wedges, emotions,
                title="감정",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                prop={'family': 'AppleGothic'})
        
        # 텍스트 스타일 설정
        plt.setp(autotexts, size=8, weight="bold", fontfamily='AppleGothic')
        plt.setp(texts, size=10, fontfamily='AppleGothic')
        
        # 레이아웃 조정
        self.figure.tight_layout()
        
        # 차트 업데이트
        self.canvas.draw()

    def goto_result(self):
        self.S = analysis_tool_result.MainView(self.data_after_logic_book, self.data_after_logic_movie)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    sys.exit(app.exec_())
