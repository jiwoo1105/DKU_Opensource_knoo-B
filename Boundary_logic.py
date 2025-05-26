#감정들의 매핑 자료구조 -> 딕셔너리 등으로 구현/ value 부분은 list로 할당
#admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment,
#disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride,
#realization, relief, remorse, sadness, surprise, neutral
all_emo_map = {
    'admiration' : [], 'admiration' : [], 'anger' : [], 'annoyance' : [], 'approval' : [] , 'caring' : [], 'confusion' : [], 'curiosity' : [], 'desire' : [],
    'disappointment' : [], 'disapproval' : [], 'disgust' : [], 'embarrassment' : [], 'excitement': [], 'fear' : [], 'gratitude' : [], 'grief' : [], 
    'joy' : [], 'love' : [], 'nervousness' : [], 'optimism' : [], 'pride' : [], 'realization' : [], 'relief' : [], 'remorse': [], 'sadness' : [], 
    'surprise' : [], 'neutral' : []
}

#user의 감정 분석 결과를 받아와서 처리하는 함수
#기존에 정의한 book db의 조회 가능 감정을 이용해서 
#감정 매핑 및 필터링 
def user_emo_logic_book():
    emo_list = []
    return emo_list

#기본적으로 user_emo_logic_book과 같은 logic
#movie 처리의 경우 줄거리에 대한 분석 결과를 이용해서 추가 정제
def user_emo_logic_movie():
    emo_list = []
    return emo_list


#비슷한 감정 처리 로직
def similar_emo_logic(emotions_dict):
    """
    비슷한 감정 추출 함수 (높은 점수부터)
    :param emotions_dict: 감정:점수 딕셔너리
    :return: 바운더리 조건을 만족하는 가장 높은 감정들의 딕셔너리
    """
    # 감정들을 점수 기준으로 내림차순 정렬
    sorted_emotions = sorted(emotions_dict.items(), key=lambda x: x[1], reverse=True)
    
    # 결과를 저장할 딕셔너리
    result = {}
    
    # 첫 번째 감정은 무조건 포함
    result[sorted_emotions[0][0]] = sorted_emotions[0][1]
    
    # 이전 감정의 점수
    prev_score = sorted_emotions[0][1]
    
    # 바운더리 값
    BOUNDARY = 0.005
    
    # 두 번째 감정부터 순회하면서 바운더리 체크
    for emotion, score in sorted_emotions[1:]:
        # 현재 감정과 이전 감정의 점수 차이가 바운더리 이하인 경우만 포함
        if prev_score - score <= BOUNDARY:
            result[emotion] = score
        else:
            break
        prev_score = score
    
    return result

#book과 movie의 경우 분리?
#반대 감정 추출 
#반대 되는 감정들의 가장 낮은 값을 리턴
def reverse_emo_logic(emotions_dict):
    """
    반대되는 감정 추출 함수 (낮은 점수부터)
    :param emotions_dict: 감정:점수 딕셔너리
    :return: 바운더리 조건을 만족하는 가장 낮은 감정들의 딕셔너리
    """
    # 감정들을 점수 기준으로 오름차순 정렬
    sorted_emotions = sorted(emotions_dict.items(), key=lambda x: x[1])
    
    # 결과를 저장할 딕셔너리
    result = {}
    
    # 첫 번째 감정은 무조건 포함
    result[sorted_emotions[0][0]] = sorted_emotions[0][1]
    
    # 이전 감정의 점수
    prev_score = sorted_emotions[0][1]
    
    # 바운더리 값
    BOUNDARY = 0.005
    
    # 두 번째 감정부터 순회하면서 바운더리 체크
    for emotion, score in sorted_emotions[1:]:
        # 현재 감정과 이전 감정의 점수 차이가 바운더리 이하인 경우만 포함
        if score - prev_score <= BOUNDARY:
            result[emotion] = score
        else:
            break
        prev_score = score
    
    return result

# 테스트용 메인 함수
if __name__ == "__main__":
    # 테스트 데이터
    emotions = {
        '중립': 0.5543,
        '행복': 0.5511,
        '슬픔': 0.0275,
        '분노': 0.0075,
        '당황': 0.0050,
        '혐오': 0.0032,
        '불안': 0.0015
    }
    
    # 반대 감정 추출 (낮은 점수부터)
    reverse_result = reverse_emo_logic(emotions)
    print("=== 반대 감정 추출 결과 ===")
    for emotion, score in reverse_result.items():
        print(f"{emotion}: {score:.4f}")
        
    # 비슷한 감정 추출 (높은 점수부터)
    print("\n=== 비슷한 감정 추출 결과 ===")
    similar_result = similar_emo_logic(emotions)
    for emotion, score in similar_result.items():
        print(f"{emotion}: {score:.4f}")



