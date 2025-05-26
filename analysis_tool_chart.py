import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import analysis_tool_result
import Boundary_logic as logic
from PySide2.QtWebEngineWidgets import QWebEngineView

class MainView(QMainWindow):
    global user_emotion_result
    #logic을 통해 잘 정제된 데이터 -> result로 넘겨서 추천 결과 출력 
    global data_after_logic_book
    global plot_result

    def __init__(self,user_emotion_result = None):
        super().__init__()
        #사용자 감정 분석된 결과 넘겨받기
        self.user_emotion_result = user_emotion_result

        self.setupUI()
        
    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_chart.ui")) # ui파일 오픈

        UI_set.goto_result.clicked.connect(self.goto_result) #최종 결과창으로의 이벤트 연결

        self.setCentralWidget(UI_set)
        self.setWindowTitle("감정에 대한 분석 차트")
        self.resize(510, 350)
        self.show()

    #logic을 이용해서 감정 분석 결과를 후처리
    def do_emo_logic(self):
        result = []
        self.data_after_logic_book
    
    #차트 분석 결과 출력 함수
    def show_result(self):
        UI_set.Show_user_emotion.setText(self.user_emotion_result)
        UI_set.Show_result_by_chart.setHtml(plot_result)

    #mylist에 저장된 값을 이용해서 chart에 plotly를 이용해 그릴 예정
    #plotly와 관련된 연결부분 함수 필요 ex) def make_chart(self): ~~
    #결과물은 plot_result라는 전역변수 저장후 show_result함수로 출력
    def get_plot_result(self):
         self.plot_result = 0

    #결과 창으로 이동
    def goto_result(self):
        self.S = analysis_tool_result.MainView(self.data_after_logic)


# 파일 경로

# pyinstaller로 원파일로 압축할때 경로 필요함

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainView()

    # main.show()

    sys.exit(app.exec_())
