import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_start_keyboard() -> ReplyKeyboardMarkup:
    button_crt = KeyboardButton('Создать новую таблицу')
    button_view = KeyboardButton('Выбрать существующую таблицу')

    reply_kbd = ReplyKeyboardMarkup(resize_keyboard=True).add(button_crt).add(button_view)

    return reply_kbd