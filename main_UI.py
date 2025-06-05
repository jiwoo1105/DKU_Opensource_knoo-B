import sys

import os

from PySide2 import QtUiTools, QtGui

from PySide2.QtWidgets import QApplication, QMainWindow

import analysis_tool_main
#import Find_info_main


class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/main.ui"))

        #2개의 버튼을 각각의 창으로 연결 -> 1) 감정 분석 창 , 2) 정보 검색 창
        #UI_set.Analysis_tool.clicked.connect(self.open_analysis)

        self.setCentralWidget(UI_set)
        # 메인 타이틀 제목
        self.setWindowTitle("추천 및 검색 프로그램")
        # 창의 사이즈 조정
        self.resize(500, 270)

        self.show()

    def open_analysis(self):
        self.S = analysis_tool_main.MainView()


    #검색기 추후 구현 예정
    #def open_Find(self):
    #   self.S = Find_info_main.MainView()


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