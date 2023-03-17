from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.addmoderator_callbackdata import send_addmoderator_callback


def generate_keyboard(from_chat_id, target_message_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить модератора", callback_data=send_addmoderator_callback.new(
                    from_chat_id=from_chat_id, message_id=target_message_id))],
        [InlineKeyboardButton(text="Отредактировать ID", callback_data='edit_moderator')],
        [InlineKeyboardButton(text="Отменить добавление модератора", callback_data='cancel_moderatorID_setup')]
    ])
    return keyboard