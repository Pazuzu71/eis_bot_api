import asyncio
import os


from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession


from config import TOKEN
from handlers import users, others


async def start_bot():
    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    # подключаем роутеры
    dp.include_router(users.router)
    dp.include_router(others.router)
    # очищаем очередь апдейтов, запускаем поулинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def is_temp_exist():
    if not os.path.exists('Temp'):
        os.mkdir('Temp')


if __name__ == '__main__':
    is_temp_exist()
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print('Ошибка, останов бота!')
