import re
import time


from aiogram import Router
from aiogram.types import Message, CallbackQuery


from utils.get_documents import get_response, get_arc_urls, download_arcs


router: Router = Router()


@router.message(lambda msg: any([
    re.fullmatch(r'\d{19}', msg.text.strip()),
    re.fullmatch(r'\d{20}', msg.text.strip()),
    re.fullmatch(r'\d{23}', msg.text.strip())]))
async def answer(msg: Message):
    await msg.reply('Ща найдем')
    response: str = await get_response(msg.text)
    urls_str, urls = await get_arc_urls(response)
    await msg.reply(urls_str)
    for i, url in enumerate(urls):
        await download_arcs(url, i)

