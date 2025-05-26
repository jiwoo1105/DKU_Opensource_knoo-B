import sys
import os
import DB_request as DB
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout


class MainView(QMainWindow):
    #책과 관련된 정리된 데이터
    global data_after_logic_book
    global data_after_logic_movie

    result_book = []
    result_movie = []
 
    def __init__(self, data_after_logic = None ,data_after_logic_movie = None):
        super().__init__()
        #chart로부터 넘겨 받은 정제된 data
        self.data_after_logic_book = data_after_logic
        self.data_after_logic_movie = data_after_logic_movie
        
        self.setupUI()
        
    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_result.ui")) # ui파일 오픈

        #결과 화면을 띄우기 위해 함수 호출
        self.show_result()

        self.setCentralWidget(UI_set)
        self.setWindowTitle("추천 결과")
        self.resize(510, 350)
        self.show()

    #최종 추천 결과를 보여주는 함수
    def show_result(self):
        self.result_book = self.get_recom_book()
        #self.result_movie = self.get_recom_movie()

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
    
    def get_recom_book(self):
        db = DB.book_db()
        # data => logic을 이용해 정제된 data
        data = self.data_after_logic_book
        result = db.lookup_all(data)

        return result
    
    def get_recom_movie(self):
        result = []

        return result

        



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
