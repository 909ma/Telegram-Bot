# === print message log.py =====================================
# 봇에 보낸 채팅으로부터 사용자의 ID와 이름, 텍스트 메세지 출력
# 이모티콘이나 사진 등은 출력하지 않는다.
# ==============================================================
# 수정시각: 2024-02-22 20:19:11

import requests

from my_key import my_bot_url


# 데이터 가져오기
response = requests.get(my_bot_url)

# JSON 데이터 파싱
data = response.json()

    # 결과 출력
for result in data['result']:
    try:
        user_id = result['message']['from']['id']
        user_name = result['message']['from']['first_name']
        message_text = result['message']['text']

        print("=" * 20)
        print(f"ID: {user_id}")
        print(f"Name: {user_name}")
        print(f"Message: {message_text}")
        print("=" * 20)
    except:
        pass