import asyncio


from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession


from config import TOKEN, CREDENTIALS
from handlers import users, others
from tools.sql import create_pool, create_tables


async def start_bot():
    pool = await create_pool(**CREDENTIALS)
    await create_tables(pool)

    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher(pool=pool)

    # подключаем роутеры
    dp.include_router(users.router)
    dp.include_router(others.router)
    # очищаем очередь апдейтов, запускаем поулинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print('Ошибка, останов бота!')
