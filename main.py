import asyncio
import logging
import sys

from bot.dispatcher import bot, dp
from bot.handlers import router

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())