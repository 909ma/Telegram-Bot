import os
# import time
import json
import random
import asyncio
import requests
# !pip install python-telegram-bot
import telegram
from bs4 import BeautifulSoup
from my_key import my_token
from datetime import datetime, timedelta


async def send_telegram_message(text, target_id):
    bot = telegram.Bot(token=my_token)
    await bot.send_message(chat_id=target_id, text=text)

async def announce(new_message):
    # JSON 파일에서 데이터 읽어오기
    with open('bot.json', 'r') as file:
        data = json.load(file)

    # 'hotdeal' 키에 해당하는 값을 가져와서 변수에 저장
    sending_id_list = data['hotdeal']

    # 새로운 메시지를 텔레그램으로 전송
    for id in sending_id_list:
        await send_telegram_message(new_message, id)
    print("announce: ", new_message)

async def parse_and_update():
    while True:
        try:
            # 웹 페이지 URL
            url = 'https://arca.live/b/hotdeal'

            # 웹 페이지에 요청을 보내고 HTML을 가져옴
            response = requests.get(url)
            html = response.text

            # BeautifulSoup을 사용하여 HTML을 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 태크 크롤링
            target_class = soup.find('a', class_='badge')  # 게시글 분류
            target_title = soup.find('a', class_='title hybrid-title')  # 게시글 제목
            target_link = soup.find('a', class_='title hybrid-title')['href']  # 게시글 링크

            # span 태그 중에서 클래스가 "comment-count"인 요소를 찾아 제거
            comment_count_span = target_title.find('span', class_='comment-count')
            if comment_count_span:
                comment_count_span.extract()

            # 개행 문자를 제거하고 내용을 출력
            target_class = target_class.text.strip()
            target_title = target_title.text.strip()

            new_message = f"[{target_class}] {target_title} - https://arca.live{target_link}"
            print("새로 파싱한 메시지:", new_message)

            # 기존 메시지 파일 읽기
            try:
                with open("hotdeal.txt", "r", encoding="utf-8") as file:
                    existing_message = file.readline().strip()
            except FileNotFoundError:
                existing_message = None

            # 새로운 메시지와 기존의 첫 줄 메시지가 다르다면 파일에 새로운 메시지를 추가
            if existing_message != new_message:
                # 기존 내용을 유지하면서 첫 줄에 새로운 메시지를 추가
                with open("hotdeal.txt", "r+", encoding="utf-8") as file:
                    content = file.read()
                    file.seek(0, 0)
                    file.write(new_message.rstrip('\r\n') + '\n' + content)

                await announce(new_message)
            else:
                # print("기존 메시지와 동일합니다.")
                pass

            break

        except Exception as e:
            # 예외 발생 시 에러 메시지 출력 후 재시도
            print(f"Error: {e}. Retrying...")
            await asyncio.sleep(5)  # 5초 대기 후 다시 시도


# =================================================================================================
async def main():
    # 시작 공지
    # await announce("서버 변경으로 장시간 작동이 중지되었습니다. 확인하세요.")
    print("start")

    while True:
        await parse_and_update()
        random_second = random.randint(60, 300) # 1분부터 5분 사이의 랜덤한 시간 생성
        next_time = datetime.now() + timedelta(seconds=random_second)
        print("Next time:", next_time, "\n")
        await asyncio.sleep(random_second)

if __name__ == "__main__":
    if not os.path.exists("hotdeal.txt"):
        with open("hotdeal.txt", "w", encoding="utf-8") as file:
            file.write("start")
    else:
        pass
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")

