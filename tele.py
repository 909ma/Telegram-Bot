import telegram
import asyncio

async def send(token, chat_id, text):
    bot = telegram.Bot(token)
    await bot.send_message(chat_id=chat_id, text=text)