import requests
import Boundary_logic as logic

#last.fm에서 받은 api발급 키와 name
API_KEY    = '99d0ccd0deee6c19efcceb20c52b1a66'
USER_AGENT = 'lime/1.0' # lime
BASE_URL   = 'https://ws.audioscrobbler.com/2.0/'

headers = {
    'user-agent': USER_AGENT
}

# 임시 data // emo_list는 나중에 감정 처리된 값으로 받아올 예정
emotion = 'happy'
emo_list = ['happy','sad']

#emo_list = logic.user_emo_logic()

#단일 page 조회
def lookup_page(emotion):
    tracks  = []
    params = {
        'method'  : 'tag.getTopTracks',
        'tag'     : emotion,
        'api_key' : API_KEY,
        'format'  : 'json',
        'limit'   : 50,
    }
    req = requests.get(BASE_URL, headers=headers, params=params)
    data = req.json()
    curr = data.get('tracks', {}).get('track', [])

    tracks.extend(curr)

    return tracks

#emotion을 받아서 db 전체 순회
#return 값은 list 형식
# 매우 오래 걸림을 확인 -> 조정 필요
def db_lookup_all(emotion):
    tracks  = []
    page    = 1

    print('while loop 들어가기 전')

    #page 단위로 해당하는 emotion값에 따른 db 전체 조회
    while True:
        print('page 값:',page)
        params = {
        'method'  : 'tag.getTopTracks',
        'tag'     : emotion,
        'api_key' : API_KEY,
        'format'  : 'json',
        'limit'   : 50,
        'page'    : page
    }
        
        req = requests.get(BASE_URL, headers=headers, params=params)
        data = req.json()

        curr = data.get('tracks', {}).get('track', [])

        if not curr:
            break

        tracks.extend(curr)
        page += 1

    print('함수 종료 전')
    return tracks

#boundary를 이용해 처리된 감정들을 이용해서 각 감정들로 db 조회
def lookup_for_all_emo(emo_list):
    curr = []
    for emo in emo_list:
        track = lookup_page(emo)
        for t in track:
            t['emotion'] = emo
        curr.extend(track)
    return curr

#tracks = db_lookup_all(emotion)
tracks = lookup_for_all_emo(emo_list)
for t in tracks:
    print(f"[{t['emotion']}] {t['name']} — {t['artist']['name']}")



