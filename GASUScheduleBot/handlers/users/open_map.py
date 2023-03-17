from loader import dp
from aiogram.dispatcher.filters import Command
from states.registration import RegistrationStates
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo #test web app


@dp.message_handler(Command("openmap"), state=RegistrationStates.RegistrationComplete)
async def show_map(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Карта СПбГАСУ", web_app=WebAppInfo(url=f"https://map.spbgasu.ru")))
    await message.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                         reply_markup= markup)