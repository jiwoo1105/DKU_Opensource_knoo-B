import sys
import os
from PySide2 import QtUiTools, QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import DB_request

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        global UI_set
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/Find_info_main.ui"))
        
        # 검색 버튼 클릭 시 결과 표시
        UI_set.Find_info.clicked.connect(self.show_result)
        
        self.setCentralWidget(UI_set)
        self.setWindowTitle("정보 검색")
        self.resize(510, 650)
        self.show()

    def show_result(self):
        # 사용자 입력 텍스트 가져오기
        search_text = UI_set.user_input.text()
        
        # 입력이 비어있는 경우 처리
        if not search_text:
            UI_set.show_result.setPlainText("검색어를 입력해주세요.")
            return
            
        # 라디오 버튼 상태 확인
        is_movie = UI_set.Find_movie.isChecked()
        is_book = UI_set.Find_book.isChecked()
        
        result_text = ""
        
        # 책 검색
        if is_book:
            book_db = DB_request.book_db()
            book_results = book_db.search_and_get_book_summaries(search_text)
            
            if not book_results:
                result_text = "검색 결과가 없거나 줄거리가 제공되지 않는 책입니다."
            else:
                result_text = f"'{search_text}'을(를) 포함한 책 중 줄거리가 있는 결과 {len(book_results)}개:\n\n"
                
                for idx, (title, summary) in enumerate(book_results, start=1):
                    result_text += (
                        f"[{idx}] 제목: {title}\n"
                        f"줄거리:\n{summary}\n"
                        + "-"*40 + "\n\n"
                    )
        
        # 영화 검색
        elif is_movie:
            movie_db = DB_request.movie_db()
            movie_results = movie_db.search_and_get_movie_summaries(search_text)
            
            if not movie_results:
                result_text = "검색 결과가 없거나 줄거리가 제공되지 않는 영화입니다."
            else:
                result_text = f"'{search_text}'을(를) 포함한 영화 중 줄거리가 있는 결과 {len(movie_results)}개:\n\n"
                
                for idx, (title, director, summary) in enumerate(movie_results, start=1):
                    result_text += (
                        f"[{idx}] 제목: {title}\n"
                        f"감독: {director}\n"
                        f"줄거리:\n{summary}\n"
                        + "-"*40 + "\n\n"
                    )
        
        # 아무것도 선택되지 않은 경우
        else:
            result_text = "책 또는 영화를 선택해주세요."
        
        # 결과 표시
        UI_set.show_result.setPlainText(result_text)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainView()
    sys.exit(app.exec_())