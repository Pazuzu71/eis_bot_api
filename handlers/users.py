import os.path
import re
import time
from datetime import datetime
from zipfile import ZipFile


from aiogram import Router
from aiogram import F
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.types import Message, CallbackQuery
from asyncpg import Pool


from config import TEMP_DIR
from tools.api import get_response, download_arcs
from tools.xml import get_arc_urls, get_publication_date
from tools.sql import create_path, get_path
from utils.funcs import create_dir, find_subsystemType
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
            with ZipFile(os.path.join(WORK_DIR, f'{arc}.zip')) as z:
                z.extractall(WORK_DIR)
            os.unlink(os.path.join(WORK_DIR, f'{arc}.zip'))

        docs_dict: dict = {}
        # TODO Ключи можно сделать через лексикон
        for path, dirs, files in os.walk(WORK_DIR):
            if files:
                for file in files:
                    if file.startswith('epNotification'):
                        pass
                    elif file.startswith('epProtocol'):
                        pass
                    elif file.startswith('epNoticeApplicationsAbsence_'):
                        pass
                    elif file.startswith('contract_'):
                        eispublicationdate = get_publication_date('contract', WORK_DIR, file)
                        doc_id = await create_path(pool, WORK_DIR, file)
                        docs_dict.setdefault('Сведения о контракте (СоК)', []).append((doc_id, eispublicationdate))
                    elif file.startswith('contractProcedure_'):
                        eispublicationdate = get_publication_date('contractProcedure', WORK_DIR, file)
                        doc_id = await create_path(pool, WORK_DIR, file)
                        docs_dict.setdefault('Сведения об исполнении (СоИ)', []).append((doc_id, eispublicationdate))
        print(docs_dict)
        for doc_type in ('Сведения о контракте (СоК)', 'Сведения об исполнении (СоИ)'):
            documents = docs_dict.get(doc_type, [])
            documents = sorted([
                (doc_id, eispublicationdate)
                for doc_id, eispublicationdate in documents
            ], key=lambda x: x[1], reverse=True)
            kb = kb_creator(documents[:81])
            await msg.reply(text=f'{doc_type}: {msg.text}', reply_markup=kb)
    else:
        await msg.reply(response)


@router.callback_query(F.data.startswith('document_'))
async def get_document(callback: CallbackQuery, pool: Pool, bot: Bot):
    doc_id = callback.data.split('_')[-1]
    doc_id = int(doc_id)
    await callback.answer(text=f'id файла в базе {doc_id}')
    path = await get_path(pool, doc_id)
    sending_file = FSInputFile(path)
    await bot.send_document(chat_id=callback.from_user.id,
                            document=sending_file,
                            reply_to_message_id=callback.message.message_id)
