from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram import Bot, types


main_key = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
        .add(KeyboardButton(text='🗓Расписание')) \
        .add(KeyboardButton(text='🗺Карта СПбГАСУ')) \
        .add(KeyboardButton(text='🌐Полезные ссылки'))


