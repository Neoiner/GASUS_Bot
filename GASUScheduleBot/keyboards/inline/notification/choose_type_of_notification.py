from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def generate_keyboard(from_chat_id, target_message_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Для факультета", callback_data='for_faculty')],
        [InlineKeyboardButton(text="Для групп (одной или несколько)", callback_data='for_group')],
        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
    ])
    return keyboard