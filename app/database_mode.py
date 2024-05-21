import aiohttp
import dotenv
import os

from content import db_data

dotenv.load_dotenv()


async def send_request(request: dict, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=request) as response:
            try:
                response_json = await response.json()
                if response_json['status'] is False:
                    return '-'
                resp = response_json['answer']
                if resp == '':
                    return '-'
                return resp

            except Exception as e:
                print('error', e)
                return '-'


async def get_db_answer(question):
    data = {
        'database': db_data,
        'question': question,
        'answer_format': '',
        'positions_count': 3,
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'classification_error_message': 'К сожалению ничего не было найдено!',
        'detecting_error_message': 'К сожалению ничего не было найдено!',
    }

    return await send_request(
        request=data,
        url='http://85.193.95.151:11111/'
    )
