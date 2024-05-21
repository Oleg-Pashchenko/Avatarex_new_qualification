import json
import os
from openai import AsyncOpenAI
import asyncio
import dotenv

import settings
from app.exceptions import JsonParseError

dotenv.load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def get_response(messages, model="gpt-4o"):
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(str(e))


async def get_memory(messages: list[dict], attempt=1):
    messages.append({'role': 'user', 'content': '/memory'})
    memory_answer = await get_response(messages)
    memory_answer = memory_answer.replace('`', '').replace('json', '').replace("'", '"')
    try:
        data = json.loads(memory_answer)['user_memory']
       #  messages.pop(-1)
        return data
    except:
        # messages.pop(-1)
        if attempt > 3:
            raise JsonParseError()
        return await get_memory(messages[:-1], attempt + 1)


async def reset(messages: list[dict]):
    messages.append({'role': 'user', 'content': '/reset'})
    await get_response(messages)
    # messages.pop(-1)


async def get_classification_function():
    properties = {'is_user_need_more': {'type': 'boolean',
                                        'description': 'Хочет ли user найти что-то еще исходя из его последнего сообщения?'}}

    return [{
        "name": "is_user_need_more",
        "description": "Хочет ли user найти что-то еще исходя из его последнего сообщения?",
        "parameters": {
            "type": "object",
            "properties": properties,
            'required': ['is_user_need_more']
        }
    }]


async def is_user_need_more(messages):
    try:

        messages = [
            {'role': 'system', 'content': 'Хочет ли user найти что-то еще? Заполни is_user_need_more'},
            messages[-2],
            messages[-1]
        ]
        completion = await client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            functions=await get_classification_function(),
            function_call={"name": "is_user_need_more"},
            timeout=30
        )
        return json.loads(completion.choices[0].message.function_call.arguments)['is_user_need_more']
    except Exception as e:
        print(e)
        return True
