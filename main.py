import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from handlers import router
from subscribed_request import subscribed_task


TOKEN = getenv('BOT_TOKEN')
dp = Dispatcher()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.include_router(router)
    task = asyncio.create_task(subscribed_task(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


