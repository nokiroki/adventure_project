import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from telegram_api.utils import get_start_keyboard

with open('api_token.txt') as f:
    API_TOKEN = f.read()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я твой удобный бот для ведения таблицы долгов. Что ты хочешь?",
        reply_markup=get_start_keyboard()    
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
