from aiogram.utils.callback_data import CallbackData


# callbackdata's name(1st param) is shorted to not exceed limit of 64bytes
diffgroup_schedule_callback = CallbackData("diffg_sc", "is_weekday", "group", "weektype", "weekday", "time")