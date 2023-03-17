from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.send_notification_callbackdata import send_notification_callback


def generate_keyboard(from_chat_id, target_message_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать рассылку", callback_data=send_notification_callback.new(
                    from_chat_id=from_chat_id, message_id=target_message_id))],
        [InlineKeyboardButton(text="Отредактировать сообщение", callback_data='edit_notification')],
        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
    ])
    return keyboard