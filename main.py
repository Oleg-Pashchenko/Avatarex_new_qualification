import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import dotenv
import settings
from app.database_mode import get_db_answer

from app.exceptions import UserMemoryNotFound, CrmFieldNotFound, JsonParseError
from app.prompt_mode import get_response, get_memory, reset, is_user_need_more
from content import fields
from settings import qualification_finished_message

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
history = {}
blocked_users = []


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    history[message.chat.id] = [{"role": "system", "content": settings.get_prompt(fields)}]
    if message.chat.id in blocked_users:
        blocked_users.pop(blocked_users.index(message.chat.id))
    await message.answer(settings.salesbot_message)


@dp.message()
async def conversation(message: types.Message):
    if message.chat.id not in history.keys():
        return await cmd_start(message)
    try:
        messages = history[message.chat.id]
        last_q = ''
        for message in messages[::-1]:
            if message['content'] != '/memory':
                last_q = message['content']
                break
        if len(messages) > 0 and last_q == qualification_finished_message:
            print('yes')
            q = await is_user_need_more(messages)
            print(q)
            if not q:
                blocked_users.append(message.chat.id)
                return await message.answer("Понял вас! Если захотите заново пообщаться напишите /start !")

        messages.append({'role': 'user', 'content': message.text})
        gpt_answer = await get_response(messages)
        messages.append({"role": "assistant", "content": gpt_answer})
        if message.text == '/memory':
            return await message.answer(settings.memory_message)

        history[message.chat.id] = messages

        memory_answer = await get_memory(messages)
        is_qualification_ended, message_to_db = settings.is_qualification_finished(memory_answer, fields)
        if is_qualification_ended is True:
            db_answer = await get_db_answer(message_to_db)
            messages.append({'role': 'assistant', 'content': db_answer})
            messages.append({'role': 'assistant', 'content': qualification_finished_message})
            await reset(messages)
            await message.answer(db_answer)
            await message.answer(qualification_finished_message)
            history[message.chat.id] = messages
        else:
            await message.answer(gpt_answer)
            # await message.answer('ОТЛАДОЧНОЕ СООБЩЕНИЕ: ' + str(type(memory_answer)) + ' ' + str(memory_answer))

    except (UserMemoryNotFound, CrmFieldNotFound, JsonParseError) as e:
        await message.answer(str(e))
    except Exception as e:
        print(e)
        await message.answer(f"Повторите запрос позднее!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
