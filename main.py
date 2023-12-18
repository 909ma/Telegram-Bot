import telegram
import requests
import asyncio
import json
from my_key import *

async def send(text):
    bot = telegram.Bot(my_token)
    await bot.send_message(my_chat, text=text)

def read():
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

async def main():
    message_text = "main 테스트입니다2"
    await send(message_text)
    read()

# asyncio.run(main())  # 주석 처리한 이유는 Jupyter Notebook 등에서 실행 시 asyncio.run()을 사용하면 에러가 발생할 수 있음

# 이 코드를 사용하려면 다음과 같이 실행하십시오.
asyncio.get_event_loop().run_until_complete(main())
