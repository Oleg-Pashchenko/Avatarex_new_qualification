import json
import os
from openai import AsyncOpenAI
import asyncio
import dotenv

import settings

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
        return json.loads(memory_answer)['user_memory']
    except:
        if attempt > 3:
            raise settings.JsonParseError()
        return await get_memory(messages[:-1], attempt + 1)


async def reset(messages: list[dict]):
    messages.append({'role': 'user', 'content': '/reset'})
    await get_response(messages)
