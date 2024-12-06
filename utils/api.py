import uuid


import aiohttp
import aiofiles
import time


async def get_response(subsystemType: str, eisdocno: str):
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
                <subsystemType>{subsystemType}</subsystemType>
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
        print('________________________')
        print(response)
        print('________________________')
        return response, 1
    except Exception as response:
        print('________________________')
        print(response)
        print('________________________')
        return str(response), 0


async def download_arcs(WORK_DIR: str, url: str, arc_name: str):
    async with aiohttp.ClientSession() as client:
        async with client.get(url, ssl=True) as response:
            cnt_break = 0
            while True:
                time.sleep(5)
                print(arc_name, response.status)
                if response.status == 200:
                    out = await aiofiles.open(f'{WORK_DIR}//{arc_name}.zip', mode='wb')
                    await out.write(await response.read())
                    await out.close()
                    return True
                else:
                    cnt_break += 1
                if cnt_break >= 10:
                    print(cnt_break, 'Ошибка cnt 10')
                    return False
