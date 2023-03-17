from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Расписание каждый день", callback_data=subscription_preferences_callback.new(
        type="daily", subtype="none", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="Расписание 1 раз в неделю", callback_data=subscription_preferences_callback.new(
        type="weekly", subtype="none", time="none", group="none", set=0))],
    [InlineKeyboardButton(text="Отменить настройку подписки", callback_data='cancel_subscription_setup')]
])