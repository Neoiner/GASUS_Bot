from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.survey_callbackdata import survey_callback

def generate_keyboard(survey_options, admin_chat_id="show_test", message_id="show_test"):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    option_number = 1
    for survey_option in survey_options:
        row = []
        row.append(InlineKeyboardButton(text=survey_option, callback_data=survey_callback.new(
            admin_chat_id=admin_chat_id, message_id=message_id, option=option_number)))
        option_number += 1
        keyboard.inline_keyboard.append(row)

    return keyboard
