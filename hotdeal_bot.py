# === hotdeal_bot.py =========================================
# 아카라이브의 핫딜에서 최신 게시글 하나를 긁어온다.
# 새롭게 긁기 전에 두 개 이상 게시글 올라오면 하나만 긁어온다.
# ============================================================
# 수정시각: 2024-02-22 22:15:46

import os
import time
import json
import random
import asyncio
import requests
import telegram
from bs4 import BeautifulSoup
from my_key import my_token, my_chat

async def send_telegram_message(text, target_id):
    bot = telegram.Bot(token=my_token)
    await bot.send_message(chat_id=target_id, text=text)

async def parse_and_update():
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

        # print("새로운 메시지를 파일에 추가했습니다.")
            print("전송")

        # JSON 파일에서 데이터 읽어오기
        with open('bot.json', 'r') as file:
            data = json.load(file)

        # 'hotdeal' 키에 해당하는 값을 가져와서 변수에 저장
        sending_id_list = data['hotdeal']

        # 새로운 메시지를 텔레그램으로 전송
        for id in sending_id_list:
            await send_telegram_message(new_message, id)

        # 새로운 메시지를 텔레그램으로 전송
        # for id in my_chat:
        #     await send_telegram_message(new_message, id)
    else:
        # print("기존 메시지와 동일합니다.")
        pass

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

async def main():
    # await announce("점검을 위해 잠시 기능 종료.")

    # 시작 공지
    await announce("점검 완료. 제대로 기능할 겁니다.")

    while True:
        await parse_and_update()
        random_second = random.randint(60, 300) # 1분부터 5분 사이의 랜덤한 시간 생성
        print(random_second)
        await asyncio.sleep(random_second)

if __name__ == "__main__":
    with open("hotdeal.txt", "w", encoding="utf-8") as file:
        file.write("start")
    asyncio.run(main())
