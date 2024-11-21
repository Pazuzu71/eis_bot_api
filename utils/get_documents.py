import uuid
import xml.etree.ElementTree as ET


import asyncio
import aiohttp
import aiofiles
import time


async def get_response(eisdocno: str):
    """Эта фукнция запрашивает данные в ЕИС по реестровому номеру"""
    endpoint = 'https://int44.zakupki.gov.ru/eis-integration/services/getDocsLE2'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'accept': '*/*'
    }
    body = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ws="http://zakupki.gov.ru/fz44/get-docs-le/ws">
       <soapenv:Header/>
       <soapenv:Body>
          <ws:getDocsByReestrNumberRequest>
             <index>
                <id>{uuid.uuid4()}</id>
                <createDateTime>2024-10-30T10:38:07.553</createDateTime>
                <mode>PROD</mode>
             </index>
             <selectionParams>
                <subsystemType>RGK</subsystemType>
                <reestrNumber>{eisdocno}</reestrNumber>
             </selectionParams>
          </ws:getDocsByReestrNumberRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    try:
        async with aiohttp.ClientSession() as client:
            response = await client.post(url=endpoint, data=body, headers=headers, ssl=False)
        response = await response.text()
        print(response)
        return response, 1
    except Exception as response:
        print('________________________')
        print(response)
        print('________________________')
        return str(response), 0
    # except aiohttp.client_exceptions.ClientConnectorError:
    #     print(aiohttp.client_exceptions.ClientConnectorError, 'Ошибка доступа к int44.zakupki.gov.ru:443')
    #     return 'Error'


async def get_arc_urls(xml: str):
    """Эта функция вытаскивает ссылки на архивы их ответа"""
    # TODO нужно обработать исключения, когда файла нет, и другие левые ответы
    root = ET.fromstring(xml)
    urls = [url.text for url in root.findall('.//archiveUrl')]
    if urls:
        return '\n'.join(urls), urls
    no_data = root.findall('.//noData')
    if no_data and no_data[0].text == 'true':
        return 'Нет данных', []
    elif no_data:
        return no_data[0].text
    return 'Что-то пошло не так', []


async def download_arcs(WORK_DIR: str, url: str, eis_docno: str, i: int):
    async with aiohttp.ClientSession() as client:
        async with client.get(url, ssl=True) as response:
            cnt_break = 0
            while True:
                time.sleep(2)
                print(i, response.status)
                if response.status == 200:
                    out = await aiofiles.open(f'{WORK_DIR}//{eis_docno}_{i}.zip', mode='wb')
                    await out.write(await response.read())
                    await out.close()
                    break
                else:
                    cnt_break += 1
                if cnt_break >= 10:
                    print(cnt_break, 'Ошибка cnt 10')
                    break

# async def main():
#     xml = await get_response('2713250003424000003')
#     urls = await get_arc_urls(xml)
#     print(urls)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
