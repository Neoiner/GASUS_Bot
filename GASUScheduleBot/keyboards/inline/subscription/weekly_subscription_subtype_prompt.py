from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В воскресенье", callback_data=subscription_preferences_callback.new(
        type="weekly", subtype="sunday", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="В понедельник", callback_data=subscription_preferences_callback.new(
        type="weekly", subtype="monday", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="Отменить настройку подписки", callback_data='cancel_subscription_setup')]
])