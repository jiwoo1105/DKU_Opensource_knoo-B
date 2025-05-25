from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# 모델 이름
model_name = "monologg/kocharelectra-base-finetuned-goemotions"

# 모델과 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# config에서 id2label 자동 불러오기
id2label = model.config.id2label  

# 사용자 입력
text = input("감정 분석할 문장을 입력하세요: ")

# 전처리
inputs = tokenizer(text, return_tensors="pt")

# 예측 (멀티레이블 → sigmoid)
with torch.no_grad():
    outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits)

# 결과 출력 (0.3 이상 감정만)
threshold = 0.3
results = []

for i, prob in enumerate(probs[0]):
    if prob >= threshold:
        label_name = id2label[i]  
        results.append((label_name, float(prob)))

# 출력
print("\n[감정 분석 결과]")
for label, score in sorted(results, key=lambda x: -x[1]):
    print(f"{label}: {score:.4f}")

