from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="НЕТ", callback_data="abort_change_group"),
     InlineKeyboardButton(text="ДА", callback_data="proceed_change_group")]
])
