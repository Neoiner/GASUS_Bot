from aiogram.utils.callback_data import CallbackData


# callbackdata's name(1st param) is shorted to not exceed limit of 64 symbols
subscription_preferences_callback = CallbackData("subscr_pref", "type", "subtype", "time", "group", "set")