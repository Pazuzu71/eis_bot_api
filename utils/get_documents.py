import uuid


import asyncio
import aiohttp


async def get_document(eisdocno: str):
    endpoint = 'https://int44.zakupki.gov.ru/eis-integration/services/getDocsLE2'
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    #     'accept': '*/*'
    # }
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
    '''.encode('utf-8')

    async with aiohttp.ClientSession() as client:
        response = await client.post(url=endpoint, data=body, ssl=False)
    return await response.text()


async def main():
    r = await get_document('2713250003424000003')
    print(r)


if __name__ == '__main__':
    asyncio.run(main())
