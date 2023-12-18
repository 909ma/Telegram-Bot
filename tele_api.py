import telegram
import asyncio
from my_key import *

html = f"https://api.telegram.org/bot{my_token}/getUpdates"

async def main():
    token = my_token
    bot = telegram.Bot(token)
    await bot.send_message(chat_id = my_chat, text="안녕하세요. 반갑습니다.")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
