from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.inline import share_schedule
from loader import dp
from states.registration import RegistrationStates
from utils.db_api.methods.schedule_methods import get_week_schedule_by_userid1, get_week_info
from utils import schedule_to_text
from aiogram.utils.markdown import hbold


@dp.message_handler(Command("week"), state=RegistrationStates.RegistrationComplete)
async def show_week_schedule(message: Message):
    user_id = message.from_user.id
    week_schedules = await get_week_schedule_by_userid1(user_id=user_id)
    current_week_name = (await get_week_info())[1]
    await message.answer(text=f"Текущая неделя - {hbold(current_week_name)}\n\n"
                              f"Расписание на текущую неделю:")
    
    for schedule in week_schedules:
        await message.answer(text=schedule, reply_markup=share_schedule.generate_keyboard(""))
