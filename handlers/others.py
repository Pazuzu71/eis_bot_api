from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router


router: Router = Router()


@router.message()
async def echo(msg: Message):
    await msg.reply(msg.text)
