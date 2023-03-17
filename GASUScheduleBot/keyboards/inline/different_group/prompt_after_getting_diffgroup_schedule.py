from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.redirect_to_diffgroup_schedule_selection_callbackdata import redirect_to_schedule_selection_callback


def generate_keyboard(target_group_name):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Узнать другое расписание {target_group_name}", callback_data=redirect_to_schedule_selection_callback.new(group_name=target_group_name))],
        [InlineKeyboardButton(text="Поделиться расписанием", switch_inline_query=target_group_name)],
        [InlineKeyboardButton(text="Отменить поиск", callback_data="abort_different_group_search")]
    ])
    return keyboard