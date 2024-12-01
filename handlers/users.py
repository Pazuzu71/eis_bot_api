import os.path
import re
import time
from datetime import datetime
from zipfile import ZipFile


from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from asyncpg import Pool


from utils.api import get_response, download_arcs
from utils.xml import get_arc_urls
from config import TEMP_DIR
from utils.funcs import create_dir, find_subsystemType, get_docs_dates
from keyboards.eis_publication_dates_kb import kb_creator


router: Router = Router()


@router.message(lambda msg: any([
    re.fullmatch(r'\d{19}', msg.text.strip()),
    re.fullmatch(r'\d{18}', msg.text.strip()),
    re.fullmatch(r'\d{23}', msg.text.strip())]))
async def answer(msg: Message, pool: Pool):
    await msg.reply('Ща найдем')
    subsystemType = find_subsystemType(msg.text)
    response, error_state = await get_response(subsystemType, msg.text)
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
        time.sleep(10)
        for i, url in enumerate(urls):
            arc_name = f'{eis_docno}_{i}'
            is_downloaded_arc = await download_arcs(WORK_DIR, url, arc_name)
            if is_downloaded_arc:
                arcs.append(arc_name)
        if len(arcs) == len(urls) and len(urls) > 0:
            await msg.reply('Архивы скачаны')
        elif len(arcs) < len(urls):
            await msg.reply('Архивы скачаны не все')
        elif len(arcs) == 0:
            await msg.reply('Архивы не скачаны')
        for arc in arcs:
            z = ZipFile(os.path.join(WORK_DIR, f'{arc}.zip'))
            z.extractall(WORK_DIR)
            z.close()
            os.unlink(os.path.join(WORK_DIR, f'{arc}.zip'))

        notifications, protocols, contracts, contract_procedures = await get_docs_dates(WORK_DIR, pool)
        print(notifications, protocols, contracts, contract_procedures)
        print(len(notifications), len(protocols), len(contracts), len(contract_procedures))
        # СоК
        if contracts:
            kb = kb_creator(contracts[:81])
            await msg.reply(text=f'Сведения о контракте (СоК): {msg.text}', reply_markup=kb)
        # СоИ
        if contract_procedures:
            kb = kb_creator(contract_procedures[:81])
            await msg.reply(text=f'Сведения об исполнении (СоИ): {msg.text}', reply_markup=kb)
    else:
        await msg.reply(response)


# @router.callback_query(F.data.startswith('document_'))
# async def send_document(callback: CallbackQuery, pool: Pool, queue: Queue):
#     xml_id = callback.data.split('_')[-1]
#     await callback.answer(text=f'id файла в базе {xml_id}')
#     ftp_path, xmlname = await get_psql_data(pool, int(xml_id))
#     await queue.put((callback.from_user.id, callback.message.message_id, ftp_path, xmlname))