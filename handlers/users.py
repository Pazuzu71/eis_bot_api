import re


from aiogram import Router
from aiogram.types import Message, CallbackQuery


from utils.get_documents import get_response, get_arc_urls


router: Router = Router()


@router.message(lambda msg: re.fullmatch(r'\d{19}', msg.text.strip()))
async def get_over_here(msg: Message):
    await msg.reply('Ща найдем')
    response: str = await get_response(msg.text)
    urls: list = await get_arc_urls(response)
    await msg.reply('\n'.join(urls))
