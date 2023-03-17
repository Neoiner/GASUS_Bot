from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Настроить подписку заново", callback_data="setup_new_subscription")],
    [InlineKeyboardButton(text="Отменить подписку", callback_data='cancel_subscription')]
])