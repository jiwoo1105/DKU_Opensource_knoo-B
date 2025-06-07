# 필요한 라이브러리 임포트
import sys
import os
from PySide2 import QtUiTools, QtGui  # Qt GUI 라이브러리
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QWidget, QLabel, QVBoxLayout
import analysis_tool_chart  # 차트 표시를 위한 모듈
from analysis import emotion_analysis  # 감정 분석 모듈

class MainView(QMainWindow):
    """
    메인 윈도우 클래스
    사용자로부터 텍스트를 입력받고 감정 분석을 시작하는 첫 화면
    """
    global genre  # 장르 선택 값 저장
    global user_emo  # 사용자 감정 분석 결과 저장

    def __init__(self):
        """
        메인 윈도우 초기화
        UI 설정 및 이벤트 핸들러 연결
        """
        super().__init__()
        self.setupUI()

    def setupUI(self):
        """
        UI 구성요소 초기화 및 설정
        - UI 파일 로드
        - 버튼 이벤트 연결
        - 윈도우 크기 및 제목 설정
        """
        global UI_set

        # ui 파일 로드 (Qt Designer로 만든 UI 파일)
        UI_set = QtUiTools.QUiLoader().load(resource_path("ui_files/analysis_tool_main.ui"))

        # 차트 분석 창으로 이동하는 버튼 이벤트 연결
        UI_set.go_chart.clicked.connect(self.goto_chart)

        # 메인 윈도우 설정
        self.setCentralWidget(UI_set)
        self.setWindowTitle("사용자 감정 입력")  # 윈도우 제목
        self.resize(800, 500)  # 윈도우 크기
        self.show()  # 윈도우 표시

    def do_analy(self):
        """
        사용자가 입력한 텍스트에 대해 감정 분석 수행
        감정 분석 결과를 user_emo 변수에 저장
        """
        # 텍스트 입력창의 내용 가져오기
        input = UI_set.user_emotion_input.toPlainText()
        # 감정 분석 수행 및 결과 저장
        self.user_emo = emotion_analysis.text_analy(input)

    def goto_chart(self):
        """
        차트 분석 창으로 이동
        - 입력 텍스트 검증
        - 감정 분석 수행
        - 차트 창 생성 및 표시
        """
        # 입력된 텍스트 가져오기
        input_text = UI_set.user_emotion_input.toPlainText()
        
        # 입력 텍스트가 비어있는지 확인
        if not input_text.strip():
            return  # 텍스트가 비어있으면 차트 창으로 이동하지 않음
            
        # 감정 분석 수행
        self.do_analy()
        
        # 새로운 차트 창 생성 및 표시
        self.S = analysis_tool_chart.MainView(self.user_emo)

    def get_user_emo(self):
        """
        감정 분석 결과 반환
        Returns:
            감정 분석 결과 딕셔너리
        """
        return self.user_emo

    def get_genre(self):
        """
        선택된 장르 반환
        Returns:
            선택된 장르 값
        """
        return self.genre

def resource_path(relative_path):
    """
    리소스 파일의 절대 경로를 반환하는 헬퍼 함수
    PyInstaller로 실행 파일 생성 시 필요
    
    Args:
        relative_path: 상대 경로
    
    Returns:
        절대 경로
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 프로그램 시작점
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Qt 애플리케이션 생성
    main = MainView()  # 메인 윈도우 생성
    sys.exit(app.exec_())  # 이벤트 루프 시작 