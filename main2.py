import asyncio
from tele import send, read
from my_key import my_token, my_chat

async def main():
    message_text = "안녕하세요. 반갑습니다."
    await send(my_token, my_chat, message_text)
    read(my_token)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
