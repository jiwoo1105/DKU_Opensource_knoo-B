#감정들의 매핑 자료구조 -> 딕셔너리 등으로 구현/ value 부분은 list로 할당
all_emo_map = {
    'admiration' : []

}

#user의 감정 분석 결과를 받아와서 처리하는 함수
# 단순히 감정 분석 결과만 필요하다면 함수 사용 x
def user_emo_logic():
    emo_list = []
    return emo_list

def music_logic(track):

    #db 조회시 

    return track

#비슷한 감정 처리 로직
def similar_emo_logic(emotions):
    return emotions

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



