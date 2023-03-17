from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_keyboard(inline_query_text):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поделиться расписанием", switch_inline_query=inline_query_text)]
    ])
    return keyboard

