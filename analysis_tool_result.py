import sys
import os
import DB_request as DB
import Boundary_logic as logic
from analysis import emotion_analysis
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout


class MainView(QMainWindow):
    #책과 관련된 정리된 데이터
    global data_after_logic_book
    global data_after_logic_movie
 
    def __init__(self, user_emotion_result=None):
        super().__init__()
        #chart로부터 넘겨 받은 정제된 data
        self.user_emotion_result = user_emotion_result
        self.do_emo_logic()

        #self.show_result()

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
        result_book = self.get_recom_book()
        result_movie = self.get_recom_movie()

        if(result_book != None):
            UI_set.recommend_book.setText(result_book)
        elif(result_book == None):
            text = "추천되는 책이 없습니다"
            UI_set.recommend_book.setText(text)
        if(result_movie != None):
            UI_set.recommend_movie.setText(result_movie)
        elif(result_movie == None):
            text = "추천되는 영화가 없습니다"
            UI_set.recommend_book.setText(text)

    #초기 화면으로 돌아가는 함수 -> 추후 구현 예정
    def goto_first(self):
        #self.S = analysis_tool_chart.MainView()
        return 0
    
    def do_emo_logic(self):
        self.data_after_logic_book = [] 
        # 책 관련 감정 로직 처리
        similar_data = logic.similar_emo_logic(self.user_emotion_result)
        reverse_data = logic.reverse_emo_logic(self.user_emotion_result)
        self.data_after_logic_book.append(similar_data)
        self.data_after_logic_book.append(reverse_data)
    
    #무시
    def get_recom_book(self):
        result  = []
        db = DB.book_db()
        # data => logic을 이용해 정제된 data
        data = self.user_emotion_result

        return result
    #구현
    def get_recom_movie(self):
        result = []
        db = DB.movie_db()
        for emo in self.data_after_logic_book:
            value = 1 # emo에서 수치값 컬럼을 받아오는 변수
            result.append(db.recom_movie(emo))

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
