from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import sys
import os

# 상위 디렉토리 경로를 시스템 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Boundary_logic import similar_emo_logic, reverse_emo_logic

# 모델 이름
model_name = "monologg/kocharelectra-base-finetuned-goemotions"

# 모델과 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# config에서 id2label 자동 불러오기
id2label = model.config.id2label  

def analyze_emotion(text):
    """
    텍스트의 감정을 분석하여 감정:점수 딕셔너리를 반환
    """
    # 전처리
    inputs = tokenizer(text, return_tensors="pt")

    # 예측 (멀티레이블 → sigmoid)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits)

    # 결과 딕셔너리 생성 (0.3 이상 감정만)
    threshold = 0.3
    emotion_scores = {}

    for i, prob in enumerate(probs[0]):
        score = float(prob)
        if score >= threshold:
            label_name = id2label[i]
            emotion_scores[label_name] = score

    return emotion_scores

def print_emotion_analysis(emotion_scores):
    """
    감정 분석 결과 출력
    """
    print("\n[감정 분석 결과]")
    for label, score in sorted(emotion_scores.items(), key=lambda x: -x[1]):
        print(f"{label}: {score:.4f}")

def print_boundary_analysis(emotion_scores):
    """
    바운더리 분석 결과 출력
    """
    # 비슷한 감정 추출
    similar_emotions = similar_emo_logic(emotion_scores)
    print("\n[유사 감정 그룹]")
    for emotion, score in similar_emotions.items():
        print(f"{emotion}: {score:.4f}")

    # 반대 감정 추출
    opposite_emotions = reverse_emo_logic(emotion_scores)
    print("\n[반대 감정 그룹]")
    for emotion, score in opposite_emotions.items():
        print(f"{emotion}: {score:.4f}")

if __name__ == "__main__":
    # 사용자 입력
    text = input("감정 분석할 문장을 입력하세요: ")
    
    # 감정 분석 수행
    emotion_scores = analyze_emotion(text)
    
    # 분석 결과 출력
    print_emotion_analysis(emotion_scores)
    
    # 바운더리 분석 결과 출력
    print_boundary_analysis(emotion_scores)

