import requests
import json
from my_key import *

# 텔레그램 봇 API 엔드포인트
telegram_api_url = f"https://api.telegram.org/bot{my_token}/"

# 최근 업데이트 확인
response = requests.get(telegram_api_url + "getUpdates")
data = response.json()
check = False

# 업데이트 중에서 메시지 추출
if data["ok"]:
    updates = data["result"]
    if updates:
        for update in updates:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "No text")

            # 메시지 출력
            if check:
                print("=" * 30)
            print(f"Chat ID: {chat_id}")
            print(f"Message Text: {text}")
            check = True
    else:
        print("No new messages")
else:
    print("Error in API response")
