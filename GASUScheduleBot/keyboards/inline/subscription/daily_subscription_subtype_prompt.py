from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback


keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="На следующий день", callback_data=subscription_preferences_callback.new(
        type="daily", subtype="next", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="На текущий день", callback_data=subscription_preferences_callback.new(
        type="daily", subtype="current", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="Отменить настройку подписки", callback_data='cancel_subscription_setup')]
])