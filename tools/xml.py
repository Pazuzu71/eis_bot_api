import xml.etree.ElementTree as ET
import os
from datetime import datetime
import pytz


async def get_arc_urls(xml: str):
    """Эта функция вытаскивает ссылки на архивы их ответа"""
    # TODO нужно обработать исключения, когда файла нет, и другие левые ответы
    root = ET.fromstring(xml)
    urls = [url.text for url in root.findall('.//archiveUrl')]
    if urls:
        return '\n'.join(urls), urls
    no_data = root.findall('.//noData')
    errorInfo = root.findall('.//errorInfo')
    if errorInfo:
        error_message = '\n'.join([m.text for m in errorInfo[0].findall('.//message')])
    if no_data and no_data[0].text == 'true':
        return 'Нет данных (noData = True)', []
    elif errorInfo and error_message:
        return error_message, []
    return 'Что-то пошло не так', []


def get_publication_date(document_type, WORK_DIR, file):
    tree = ET.parse(os.path.join(WORK_DIR, file))
    root = tree.getroot()
    if document_type in ('contract', 'contractProcedure'):
        try:
            eispublicationdate = root.find('.//{http://zakupki.gov.ru/oos/types/1}publishDate')
        except Exception as e:
            print(e)
    elif document_type in ('notification',):
        try:
            eispublicationdate = root.find('.//{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        except Exception as e:
            print(e)
    try:
        eispublicationdate = datetime.fromisoformat(eispublicationdate.text)
        eispublicationdate = eispublicationdate.astimezone(tz=pytz.timezone('Europe/Moscow'))
        return eispublicationdate
    except Exception as e:
        print(e)
