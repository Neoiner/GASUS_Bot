from aiogram.utils.callback_data import CallbackData

# callbackdata's name(1st param) is shorted to not exceed limit of 64bytes
schedule_callback = CallbackData("sh_sc", "is_weekday", "week_type", "weekday", "time")