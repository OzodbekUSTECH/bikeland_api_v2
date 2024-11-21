import asyncio
from aiogram import Dispatcher
from telegram.routers import all_routers
from config_bot import bot


async def main():
    dp = Dispatcher()
    await bot.delete_webhook()
    for router in all_routers:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')