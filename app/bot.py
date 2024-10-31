import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from celery_config import send_telegram_notification

API_TOKEN = os.getenv("API_TOKEN")

# Проверка наличия токена
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in environment variables")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для обмена сообщениями.")

@dp.message(Command("send"))
async def send_message(message: types.Message):
    user_id = message.from_user.id
    msg_content = message.text.split(maxsplit=1)

    if len(msg_content) > 1:
        content = msg_content[1]
        send_telegram_notification.delay(user_id, content)
        await message.reply("Сообщение отправлено!")
    else:
        await message.reply("Пожалуйста, укажите сообщение после команды /send.")

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())