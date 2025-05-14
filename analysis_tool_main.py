import sys

import os

from PySide2 import QtUiTools, QtGui

from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout

import analysis_tool_chart

class MainView(QMainWindow):

    value, Text = NULL

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_main.ui")) # ui파일 오픈

        UI_set.go_chart.clicked.connect(self.goto_chart) #chart 분석창으로의 이벤트 연결

        self.setCentralWidget(UI_set)
        self.setWindowTitle("사용자 감정 입력")
        self.resize(510, 350)
        self.show()

    #사용자가 입력한 text와 선택한 장르에 대해서 값을 저장
    def myvalue(self):
            #장르 선택은 추후에 삭제 가능성 있음
            #self.value = UI_set.select_genre_by_combo.currentText()
            self.Text = UI_set.user_emotion_input.toPlainText()
    
    #차트 분석 창으로 이동
    def goto_chart(self):
            self.myvalue()
            self.S = analysis_tool_chart.MainView()



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
