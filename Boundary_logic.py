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

def process_emotion_results(results):
    """
    emotion_analysis.py의 결과를 딕셔너리로 변환
    :param results: emotion_analysis.py의 결과 리스트
    :return: 감정:점수 딕셔너리
    """
    return {result['label']: result['score'] for result in results}

def reverse_emo_logic(results):
    """
    반대되는 감정 추출 함수 (낮은 점수부터)
    :param results: emotion_analysis.py의 결과 리스트 또는 감정:점수 딕셔너리
    :return: 바운더리 조건을 만족하는 가장 낮은 감정들의 딕셔너리
    """
    # 결과가 리스트인 경우 딕셔너리로 변환
    if isinstance(results, list):
        emotions_dict = process_emotion_results(results)
    else:
        emotions_dict = results
        
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

def similar_emo_logic(results):
    """
    비슷한 감정 추출 함수 (높은 점수부터)
    :param results: emotion_analysis.py의 결과 리스트 또는 감정:점수 딕셔너리
    :return: 바운더리 조건을 만족하는 가장 높은 감정들의 딕셔너리
    """
    # 결과가 리스트인 경우 딕셔너리로 변환
    if isinstance(results, list):
        emotions_dict = process_emotion_results(results)
    else:
        emotions_dict = results
        
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

def print_boundary_results(results):
    """
    바운더리 분석 결과 출력
    :param results: emotion_analysis.py의 결과 리스트
    """
    # 유사 감정 추출
    similar = similar_emo_logic(results)
    print("\n[유사 감정 그룹 (바운더리: 0.005)]")
    for emotion, score in similar.items():
        print(f"{emotion}: {score:.4f}")
        
    # 반대 감정 추출
    opposite = reverse_emo_logic(results)
    print("\n[반대 감정 그룹 (바운더리: 0.005)]")
    for emotion, score in opposite.items():
        print(f"{emotion}: {score:.4f}")

# 사용 예시:
# from analysis.emotion_analysis import text_analy
# results = text_analy("분석할 텍스트")
# print_boundary_results(results)



