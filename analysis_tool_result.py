import sys
import os
import DB_requset as DB

from PySide2 import QtUiTools, QtGui

from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout


class MainView(QMainWindow):

    result_book = None
    result_movie = None
 
    def __init__(self):
        super().__init__()

        self.setupUI()
        
    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_result.ui")) # ui파일 오픈

        #UI_set.go_chart.clicked.connect(self.goto_chart) #chart 분석창으로의 이벤트 연결
        #결과 화면을 띄우기 위해 함수 호출
        self.show_result()

        self.setCentralWidget(UI_set)
        self.setWindowTitle("추천 결과")
        self.resize(510, 350)
        self.show()

    #최종 추천 결과를 보여주는 함수
    def show_result(self):

        if(self.result_book != None):
            UI_set.recommend_book.setText(self.result_book)
        elif(self.result_book == None):
            text = "추천되는 책이 없습니다"
            UI_set.recommend_book.setText(text)
        if(self.result_movie != None):
            UI_set.recommend_movie.setText(self.result_movie)
        elif(self.result_movie == None):
            text = "추천되는 책이 없습니다"
            UI_set.recommend_book.setText(text)

    #초기 화면으로 돌아가는 함수 -> 추후 구현 예정
    def goto_first(self):
        #self.S = analysis_tool_chart.MainView()
        return 0



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
