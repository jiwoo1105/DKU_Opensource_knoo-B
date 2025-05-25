from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 모델 이름 지정
model_name = "nlp04/korean_sentiment_analysis_dataset3_best"

# 모델과 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 파이프라인 생성
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# 분석할 문장 입력
text = input("감정 분석할 문장을 입력하세요: ")

# 감정 분석 수행
result = classifier(text)[0]

# 감정 분석 (상위 7개 감정)
results = classifier(text, top_k=10)

# 결과 출력
print("\n[감정 분석 결과: 28개]")
for result in results:
    print(f"{result['label']}: {result['score']:.4f}")
