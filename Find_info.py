import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import DB_request

class MainView(QMainWindow):

    global genre
    global user_emo

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/Find_info_main.ui")) # ui파일 오픈

        UI_set.Find_info.clicked.connect(self.show_result) #chart 분석창으로의 이벤트 연결

        self.setCentralWidget(UI_set)
        self.setWindowTitle("정보 검색")
        self.resize(510, 350)
        self.show()


    def show_result(self):
        book_result = []
        movie_result = []
        #text에 포함되어 있는 문자나 단어가 포함되어 있는 모든 결과를 추천함
        Text = UI_set.user_input.text()
        #radio 버튼이 체크되었는지 true/false로 반환
        mymovie = UI_set.Find_movie.ischecked()
        mybook = UI_set.Find_book.ischecked()
        if mybook:
            book_db = DB_request.book_db()
            #책 줄거리 조회
            #책의 title과 줄거리를 합쳐서 저장
            UI_set.show_result.setPlainText(book_result)
        if mymovie : 
            self.movie_db = DB_request.movie_db()
            #영화 줄거리 조회
            #영화의 title과 줄거리를 합쳐서 저장
            UI_set.show_result.setPlainText(movie_result)
        if not mymovie and not mybook:
            text = "책 or 영화를 선택해주세요"
            UI_set.show_result.setPlainText(text)

        
        

        
        

        
        

        


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

    sys.exit(app.exec)