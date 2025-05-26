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
def similar_emo_logic(emotions):
    return emotions

#book과 movie의 경우 분리?
#반대 감정 추출 
#반대 되는 감정들의 가장 낮은 값을 리턴
def reverse_emo_logic(all_emo_map):
    emotions = all_emo_map
    user_emo = user_emo_logic()

    #map들을 이용해서 user 감정을 반대로 매핑
    #따로 함수로?

    setA = set(emotions)
    setB = set(user_emo)

    result_emotions = [x for x in setB if x in setA]

    #data set을 low_value 기준으로 정렬
    result_emotions.sort(key=lambda x: min(x['scores']))
    result = result_emotions[0]

    return result



