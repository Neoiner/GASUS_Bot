from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data.config import TIMEZONE
from keyboards.inline import share_schedule
from loader import dp
from states.registration import RegistrationStates
from utils.db_api.methods.schedule_methods import get_day_schedule_by_userid1, get_week_info
from utils import schedule_to_text
from utils.map_api.map_methods import get_path_classes
import datetime


@dp.message_handler(Command("tomorrow"), state=RegistrationStates.RegistrationComplete)
async def show_tomorrow_schedule(message: Message):
    # weekday is number 0-6(monday-sunday), we increment it, so it is 1-7
    now = datetime.datetime.now(TIMEZONE)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday() + 1

    if(tomorrow_weekday == 7):
        await message.answer(text="Завтра воскресенье, занятий нет!\n"
                                  "Хороших выходных!")
    
    else:
        
        if (tomorrow_weekday == 1):
            week_type = await get_week_info(True)
            user_id = message.from_user.id
            schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=tomorrow_weekday, week_type=week_type)
        else:
            user_id = message.from_user.id
            schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=tomorrow_weekday)
        
        await message.answer(text=f"Расписание на завтра:\n{schedule}", reply_markup=share_schedule.generate_keyboard(""))
        await message.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                             reply_markup=await get_path_classes(schedule))