from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.send_notification_callbackdata import send_notification_callback


keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать рассылку опроса", callback_data='send_survey')],
        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_survey')]
    ])
