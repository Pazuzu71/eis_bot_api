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

        arcs = []
        for i, url in enumerate(urls):
            time.sleep(1)
            arc_name = f'{eis_docno}_{i}'
            is_success_downloaded = await download_arcs(WORK_DIR, url, eis_docno, i, arc_name)
            if is_success_downloaded:
                arcs.append(arc_name)
        if len(arcs) == len(urls) and len(urls) > 0:
            await msg.reply('Архивы скачаны')
        elif len(arcs) < len(urls):
            await msg.reply('Архивы скачаны не все')
        elif len(arcs) == 0:
            await msg.reply('Архивы не скачаны')

    else:
        await msg.reply(response)
