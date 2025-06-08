import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import DB_request
import os

class MainView(QMainWindow):

    global genre
    global user_emo

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        global UI_set

        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/Find_info_main.ui")) # ui파일 오픈

        UI_set.Find_info.clicked.connect(self.show_result) #검색 결과 보여주기

        self.setCentralWidget(UI_set)
        self.setWindowTitle("정보 검색")
        self.resize(510, 350)
        self.show()


    def show_result(self):
        #text에 포함되어 있는 문자나 단어가 포함되어 있는 모든 결과를 추천함
        Text = UI_set.user_input.text()
        #radio 버튼이 체크되었는지 true/false로 반환
        mymovie = UI_set.Find_movie.ischecked()
        mybook = UI_set.Find_book.ischecked()

        if mybook:
            book_db = DB_request.book_db()
            #책 줄거리 조회
            #책의 title과 줄거리를 합쳐서 저장
            book_result = book_db.search_and_get_book_summaries(Text)
            if not book_result:
                UI_set.show_result.setPlainText("검색 결과가 없거나 줄거리가 제공되지 않는 책입니다.")
            else:
            #헤더 문자열 준비
                result_text = f"'{text}'을(를) 포함한 책 중 줄거리가 있는 결과 {len(book_result)}개:\n\n"
    
            #각 항목을 순회하며 출력용 문자열 이어 붙이기
            for idx, (title, summary) in enumerate(book_result, start=1):
                result_text += (
                    f"[{idx}] 제목: {title}\n"
                    f"줄거리:\n{summary}\n"
                    + "-"*40 + "\n"
                )
            
            #완성된 문자열을 한번에 위젯에 보여주기
            UI_set.show_result.setPlainText(result_text)

        if mymovie : 
            movie_db = DB_request.movie_db()
            #영화 줄거리 조회
            #영화의 title과 줄거리를 합쳐서 저장
            book_result = movie_db.search_and_get_movie_summaries(Text)
            if not book_result:
                UI_set.show_result.setPlainText("검색 결과가 없거나 줄거리가 제공되지 않는 책입니다.")
            else:
            #헤더 문자열 준비
                result_text = f"'{text}'을(를) 포함한 책 중 줄거리가 있는 결과 {len(book_result)}개:\n\n"
    
            #각 항목을 순회하며 출력용 문자열 이어 붙이기
            for idx, (title, summary) in enumerate(book_result, start=1):
                result_text += (
                    f"[{idx}] 제목: {title}\n"
                    f"줄거리:\n{summary}\n"
                    + "-"*40 + "\n"
                )
            #완성된 문자열을 한번에 위젯에 보여주기
            UI_set.show_result.setPlainText(result_text)
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