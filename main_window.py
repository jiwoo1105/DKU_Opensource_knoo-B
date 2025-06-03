import sys
from pathlib import Path
import webbrowser
from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTabWidget
from PySide6.QtCore import Qt
import plotly.graph_objects as go
import pandas as pd
from analysis.emotion_analysis import text_analy
from Boundary_logic import similar_emo_logic, reverse_emo_logic
from DB_request import book_db, movie_db

# UI 파일 로드
ui_file = QtCore.QFile("ui_files/analysis_tool_main.ui")
ui_file.open(QtCore.QFile.ReadOnly)
loader = QtUiTools.QUiLoader()
form_class = loader.load(ui_file)
ui_file.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = form_class
        self.ui.setupUi(self)
        
        # 버튼 연결
        self.ui.go_chart.clicked.connect(self.analyze_emotion)
        
        # DB 초기화
        self.book_database = book_db()
        self.movie_database = movie_db()
        
    def analyze_emotion(self):
        text = self.ui.user_emotion_input.toPlainText()
        
        if text:
            # 감정 분석 수행
            results = text_analy(text)
            
            # 바운더리 분석
            similar_emotions = similar_emo_logic(results)
            opposite_emotions = reverse_emo_logic(results)
            
            # 결과 창 표시
            self.result_window = EmotionResultWindow(results, similar_emotions, opposite_emotions, self.book_database, self.movie_database)
            self.result_window.show()

class EmotionResultWindow(QMainWindow):
    def __init__(self, results, similar_emotions, opposite_emotions, book_db, movie_db):
        super().__init__()
        self.setWindowTitle("감정 분석 결과")
        self.setGeometry(200, 200, 1000, 800)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 감정 분석 결과 처리
        emotions = [result['label'] for result in results]
        scores = [result['score'] for result in results]
        
        # 데이터프레임 생성
        df = pd.DataFrame({
            'Emotion': emotions,
            'Score': scores
        })
        
        # Plotly 그래프 생성
        fig = go.Figure()
        
        # 주요 감정 바 차트
        fig.add_trace(go.Bar(
            name='감정 점수',
            x=df['Emotion'],
            y=df['Score'],
            marker_color='rgb(158,202,225)',
            text=df['Score'].round(4),
            textposition='auto',
        ))
        
        # 유사 감정 하이라이트
        similar_df = pd.DataFrame(list(similar_emotions.items()), columns=['Emotion', 'Score'])
        fig.add_trace(go.Bar(
            name='유사 감정',
            x=similar_df['Emotion'],
            y=similar_df['Score'],
            marker_color='rgb(255,182,193)',
            text=similar_df['Score'].round(4),
            textposition='auto',
        ))
        
        fig.update_layout(
            title='감정 분석 결과',
            xaxis_title='감정',
            yaxis_title='점수',
            template='plotly_white',
            height=400,
            barmode='group'
        )
        
        # HTML 파일로 저장하고 브라우저로 열기
        html_path = str(Path.cwd() / "emotion_graph.html")
        fig.write_html(html_path)
        webbrowser.open('file://' + html_path)
        
        # 추천 버튼
        recommend_button = QPushButton("추천 결과 보기")
        recommend_button.clicked.connect(lambda: self.show_recommendations(similar_emotions, book_db, movie_db))
        layout.addWidget(recommend_button)
        
    def show_recommendations(self, emotions, book_db, movie_db):
        emotions_list = list(emotions.keys())
        book_recommendations = book_db.lookup_all(emotions_list)
        movie_recommendations = movie_db.lookup_all(emotions_list)
        
        self.recommend_window = RecommendationWindow(book_recommendations, movie_recommendations)
        self.recommend_window.show()

class RecommendationWindow(QMainWindow):
    def __init__(self, book_recommendations, movie_recommendations):
        super().__init__()
        self.setWindowTitle("추천 결과")
        self.setGeometry(300, 300, 800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 탭 위젯 생성
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 공통 스타일
        title_style = "font-size: 16px; font-weight: bold; color: #333;"
        item_style = "background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin: 5px;"
        
        # 책 추천 탭
        book_tab = self.create_recommendation_tab("추천 도서", book_recommendations, 
            lambda x: f"제목: {x['title']}\n저자: {x['authors']}\n평점: {x.get('avg_rating', 'N/A')}\n",
            title_style, item_style)
        tab_widget.addTab(book_tab, "도서 추천")
        
        # 영화 추천 탭
        movie_tab = self.create_recommendation_tab("추천 영화", movie_recommendations,
            lambda x: f"제목: {x}\n",
            title_style, item_style)
        tab_widget.addTab(movie_tab, "영화 추천")
    
    def create_recommendation_tab(self, title, items, format_func, title_style, item_style):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # 제목 추가
        label = QLabel(title)
        label.setStyleSheet(title_style)
        content_layout.addWidget(label)
        
        # 아이템 추가
        for item in items:
            item_label = QLabel(format_func(item))
            item_label.setStyleSheet(item_style)
            content_layout.addWidget(item_label)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        return tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 