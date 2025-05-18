import sys

import os

from PySide2 import QtUiTools, QtGui

from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout

import analysis_tool_result

class MainView(QMainWindow):

    #감정 분석을 위한 변수들
    user_emotion_result = []
    #myvalue = analysis_tool_result.value
    #myText = analysis_tool_result.Text

    def __init__(self):
        super().__init__()

        self.setupUI()
        
    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_chart.ui")) # ui파일 오픈

        UI_set.goto_result.clicked.connect(self.goto_result) #최종 결과창으로의 이벤트 연결

        self.setCentralWidget(UI_set)
        self.setWindowTitle("감정에 대한 분석 차트")
        self.resize(510, 350)
        self.show()

    #이 함수에서 goemotions의 감정 분석처리 로직을 수행하고 결과를 받을 예졍 -> 결과는 mylist에 저장
    def call_goemotions_kor(self):
        return self.user_emotion_result
    
    #mylist에 저장된 값을 이용해서 chart에 plotly를 이용해 그릴 예정
    #plotly와 관련된 연결부분 함수 필요 ex) def make_chart(self): ~~
    def show_chart_for_user(self):
         return 0

    #결과 창을 이동
    def goto_result(self):
        self.S = analysis_tool_result.MainView()

    #유저의 감정 결과 받아오는 함수
#   def getUserEmotionResult():
#      user_emotion_result = self.user_emotion_result
#      return user_emotion_result



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
