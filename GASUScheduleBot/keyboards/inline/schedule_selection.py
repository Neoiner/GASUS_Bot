from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.schedule_callbackdata import schedule_callback

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="сегодня", callback_data=schedule_callback.new(
            is_weekday="False", week_type="none", weekday="none", time="today"))
    ],
    [
        InlineKeyboardButton(text="завтра", callback_data=schedule_callback.new(
            is_weekday="False", week_type="none", weekday="none", time="tomorrow"))
    ],
    [
        InlineKeyboardButton(text="Пн ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="1", time="none")),
        InlineKeyboardButton(text="Пн ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="1", time="none"))
    ],
    [
        InlineKeyboardButton(text="Вт ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="2", time="none")),
        InlineKeyboardButton(text="Вт ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="2", time="none"))
    ],
    [
        InlineKeyboardButton(text="Ср ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="3", time="none")),
        InlineKeyboardButton(text="Ср ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="3", time="none"))
    ],
    [
        InlineKeyboardButton(text="Чт ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="4", time="none")),
        InlineKeyboardButton(text="Чт ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="4", time="none"))
    ],
    [
        InlineKeyboardButton(text="Пт ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="5", time="none")),
        InlineKeyboardButton(text="Пт ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="5", time="none"))
    ],
    [
        InlineKeyboardButton(text="Сб ЧИСЛ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="1", weekday="6", time="none")),
        InlineKeyboardButton(text="Сб ЗНАМ", callback_data=schedule_callback.new(
            is_weekday="True", week_type="0", weekday="6", time="none"))
    ],
    [
        InlineKeyboardButton(text="неделя ЧИСЛИТЕЛЬ", callback_data=schedule_callback.new(
            is_weekday="False", week_type="1", weekday="none", time="week"))
    ],
    [
        InlineKeyboardButton(text="неделя ЗНАМЕНАТЕЛЬ", callback_data=schedule_callback.new(
            is_weekday="False", week_type="0", weekday="none", time="week"))
    ]
])