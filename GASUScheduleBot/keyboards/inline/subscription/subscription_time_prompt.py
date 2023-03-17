from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback

def generate_keyboard(type, subtype, group):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="8:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="8-00", group=group, set=0)),
            InlineKeyboardButton(text="8:30", callback_data=subscription_preferences_callback.new(
                 type=type, subtype=subtype, time="8-30", group=group, set=0)),
            InlineKeyboardButton(text="9:00", callback_data=subscription_preferences_callback.new(
                 type=type, subtype=subtype, time="9-00", group=group, set=0)),
            InlineKeyboardButton(text="9:30", callback_data=subscription_preferences_callback.new(
                 type=type, subtype=subtype, time="9-30", group=group, set=0))
         ],
        [
            InlineKeyboardButton(text="10:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="10-00", group=group, set=0)),
            InlineKeyboardButton(text="10:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="10-30", group=group, set=0)),
            InlineKeyboardButton(text="11:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="11-00", group=group, set=0)),
            InlineKeyboardButton(text="11:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="11-30", group=group, set=0))
        ],
        [
            InlineKeyboardButton(text="12:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="12-00", group=group, set=0)),
            InlineKeyboardButton(text="12:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="12-30", group=group, set=0)),
            InlineKeyboardButton(text="13:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="13-00", group=group, set=0)),
            InlineKeyboardButton(text="13:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="13-30", group=group, set=0))
        ],
        [
            InlineKeyboardButton(text="14:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="14-00", group=group, set=0)),
            InlineKeyboardButton(text="14:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="14-30", group=group, set=0)),
            InlineKeyboardButton(text="15:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="15-00", group=group, set=0)),
            InlineKeyboardButton(text="15:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="15-30", group=group, set=0))
        ],
        [
            InlineKeyboardButton(text="16:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="16-00", group=group, set=0)),
            InlineKeyboardButton(text="16:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="16-30", group=group, set=0)),
            InlineKeyboardButton(text="17:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="17-00", group=group, set=0)),
            InlineKeyboardButton(text="17:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="17-30", group=group, set=0))
        ],
        [
            InlineKeyboardButton(text="18:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="18-00", group=group, set=0)),
            InlineKeyboardButton(text="18:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="18-30", group=group, set=0)),
            InlineKeyboardButton(text="19:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="19-00", group=group, set=0)),
            InlineKeyboardButton(text="19:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="19-30", group=group, set=0))
        ],
        [
            InlineKeyboardButton(text="20:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="20-00", group=group, set=0)),
            InlineKeyboardButton(text="20:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="20-30", group=group, set=0)),
            InlineKeyboardButton(text="21:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="21-00", group=group, set=0)),
            InlineKeyboardButton(text="21:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="21-30", group=group, set=0)),
        ],
        [
            InlineKeyboardButton(text="22:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="22-00", group=group, set=0)),
            InlineKeyboardButton(text="22:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="22-30", group=group, set=0)),
            InlineKeyboardButton(text="23:00", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="23-00", group=group, set=0)),
            InlineKeyboardButton(text="23:30", callback_data=subscription_preferences_callback.new(
                type=type, subtype=subtype, time="23-30", group=group, set=0))
        ],
        [InlineKeyboardButton(text="Отменить настройку подписки", callback_data='cancel_subscription_setup')]
    ])
    return keyboard
