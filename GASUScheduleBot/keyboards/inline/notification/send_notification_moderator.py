from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def generate_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать ввод сообщения для рассылки", callback_data='start_notification')],
        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
    ])

    return keyboard
