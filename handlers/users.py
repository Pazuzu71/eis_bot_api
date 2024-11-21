import re
import time
from datetime import datetime


from aiogram import Router
from aiogram.types import Message, CallbackQuery


from utils.get_documents import get_response, get_arc_urls, download_arcs
from config import TEMP_DIR
from utils.funcs import create_dir


router: Router = Router()


@router.message(lambda msg: any([
    re.fullmatch(r'\d{19}', msg.text.strip()),
    re.fullmatch(r'\d{20}', msg.text.strip()),
    re.fullmatch(r'\d{23}', msg.text.strip())]))
async def answer(msg: Message):
    await msg.reply('Ща найдем')
    response, error_state = await get_response(msg.text)
    if error_state:
        urls_str, urls = await get_arc_urls(response)
        await msg.reply(urls_str)
        dt = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        user_id = msg.from_user.id
        eis_docno = msg.text.strip()
        for DIR in [TEMP_DIR, f'{TEMP_DIR}//{user_id}', f'{TEMP_DIR}//{user_id}//{dt}_{eis_docno}']:
            create_dir(DIR)
        WORK_DIR = f'{TEMP_DIR}//{user_id}//{dt}_{eis_docno}'

        for i, url in enumerate(urls):
            time.sleep(1)
            await download_arcs(WORK_DIR, url, eis_docno, i)
    else:
        await msg.reply(response)
