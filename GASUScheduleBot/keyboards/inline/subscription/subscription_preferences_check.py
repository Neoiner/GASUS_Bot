from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback


def generate_keyboard(type, subtype, time, group):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Всё верно!", callback_data=subscription_preferences_callback.new(
            type=type, subtype=subtype, time=time, group=group, set=1))],
        [InlineKeyboardButton(text="Хочу настроить по-другому", callback_data='setup_new_subscription_preferences')],
        [InlineKeyboardButton(text="Отменить настройку подписки", callback_data='cancel_subscription_setup')]
    ])
    return keyboard