from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from states.registration import RegistrationStates
from aiogram.utils.markdown import hbold, hitalic
from utils.db_api.db_gino import db
from utils.db_api.methods.user_methods import create_user
from utils.db_api.models.user import User
from keyboards.default.main_kayboard import main_key
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
#on first start, user is set to register his group

# handler on first start from inline mode(with deeplink)
@dp.message_handler(CommandStart(deep_link="connect_user_from_inline_mode"))
async def bot_first_start(message: Message):
    await RegistrationStates.RegisterGroupFromInline.set()
    await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                              f"Вижу, ты уже хочешь воспользоваться inline mode?\n"
                              f"Для работы мне нужно зарегистрировать тебя.\n\n"
                              f"Пожалуйста, напиши мне номер своей группы.\n"
                              f"Можешь писать заглавными/строчными {hbold('русскими')} буквами, '-' ставить {hbold('не обязательно')}.\n\n"
                              f"Например, я пойму {hitalic('любой')} из этих вариантов: 3аб1, 3АБ1, 3-аб-1.")


# handler on first start from bot
@dp.message_handler(CommandStart())
async def bot_first_start(message: Message):

    await RegistrationStates.RegisterGroup.set()

    await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                              f"Для работы мне нужно зарегистрировать тебя.\n\n"
                              f"Пожалуйста, напиши мне номер своей группы.\n"
                              f"Можешь писать заглавными/строчными {hbold('русскими')} буквами, '-' ставить {hbold('не обязательно')}.\n\n"
                              f"Например, я пойму {hitalic('любой')} из этих вариантов: 3аб1, 3АБ1, 3-аб-1.")


# on returning start(user stopped bot, after some time started it), user is greeted back
@dp.message_handler(CommandStart(), state=RegistrationStates.RegistrationComplete)
async def greet_returning_user(message: Message):
    existing_user = await User.get(message.from_user.id)
    if (existing_user is None):
        await RegistrationStates.RegisterGroup.set()
        await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                                f"Для работы мне нужно {hitalic('заново')} зарегистрировать тебя.\n\n"
                                f"Пожалуйста, напиши мне номер своей группы.\n"
                                f"Можешь писать заглавными/строчными {hbold('русскими')} буквами, '-' ставить {hbold('не обязательно')}.\n\n"
                                f"Например, я пойму {hitalic('любой')} из этих вариантов: 3аб1, 3АБ1, 3-аб-1.")
    else:
        await message.answer(text=f"Привет, {message.from_user.full_name}!\n"
                              f"Рад твоему возвращению! ✌️\n\n"
                              f"Я тебя уже зарегистрировал, так что можешь "
                              f"пользоваться всем моим функционалом.\n\n"
                              f"Чтобы вспомнить мои команды, "
                              f"нажми сюда - /help", reply_markup=main_key)


