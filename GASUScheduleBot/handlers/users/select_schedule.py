import datetime
from aiogram.types import Message, CallbackQuery

from data.config import TIMEZONE
from loader import dp
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters.builtin import Command
from states.registration import RegistrationStates
from utils import schedule_to_text
from utils.db_api.methods.schedule_methods import get_day_schedule_by_userid1, get_week_schedule_by_userid1, get_week_info
from keyboards.inline import schedule_selection, share_schedule
from keyboards.callbackdatas.schedule_callbackdata import schedule_callback
from utils.map_api.map_methods import get_path_classes

@dp.message_handler(Command("selectschedule"), state=RegistrationStates.RegistrationComplete)
async def show_schedule_selection(message: Message):
    week_info = await get_week_info()
    week_type_name = week_info[1]

    await message.answer(text=f"Выбери нужный день(или всю неделю).\n\n"
                              f"Текущая неделя - {hbold(week_type_name)}",
                         reply_markup=schedule_selection.keyboard)



# _callback is appended to func name to avoid having same name as handler in today_schedule
@dp.callback_query_handler(schedule_callback.filter(is_weekday="False", time="today"), state=RegistrationStates.RegistrationComplete)
async def show_today_schedule_callback(callback: CallbackQuery):
    await callback.answer(text="Получаю расписание на сегодня")

    # weekday is number 0-6(monday-sunday), we increment it, so it is 1-7
    now = datetime.datetime.now(TIMEZONE)
    weekday = now.weekday() + 1

    if(weekday == 7):
        await callback.message.answer(text="Хэй, сегодня воскресенье, занятий нет!\n"
                                           "Тусуем 🤘🤘🤘")
    else:
        # callback's origin message was sent by bot(message with schedule selection keyboard),
        # so, to get user_id, we can get chat_id  (in pm with bot, chat_id = user_id)
        user_id = callback.message.chat.id
        schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=weekday)
        await callback.message.answer(text="Расписание на сегодня:")

        await callback.message.answer(text=schedule, reply_markup=share_schedule.generate_keyboard(""))
        await callback.message.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                             reply_markup=await get_path_classes(schedule))


# _callback is appended to func name to avoid having same name as handler in tomorrow_schedule
@dp.callback_query_handler(schedule_callback.filter(is_weekday="False", time="tomorrow"), state=RegistrationStates.RegistrationComplete)
async def show_tomorrow_schedule_callback(callback: CallbackQuery):
    await callback.answer(text="Получаю расписание на завтра")

    # weekday is number 0-6(monday-sunday), we increment it, so it is 1-7
    now = datetime.datetime.now(TIMEZONE)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday() + 1

    if(tomorrow_weekday == 7):
        await callback.message.answer(text="Хэй, завтра воскресенье, занятий нет!\n"
                                           "Тусуем 🤘🤘🤘")
    else:
        user_id = callback.message.chat.id
        schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=tomorrow_weekday)
        await callback.message.answer(text=f"Расписание на завтра:{schedule}",
                                      reply_markup=share_schedule.generate_keyboard(""))
        await callback.message.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                             reply_markup=await get_path_classes(schedule))


@dp.callback_query_handler(schedule_callback.filter(is_weekday="True"), state=RegistrationStates.RegistrationComplete)
async def show_weekday_schedule(callback: CallbackQuery, callback_data: dict):
    target_weekday = int(callback_data.get("weekday"))
    target_weektype = []
    if callback_data.get("week_type") == "1":
        target_weektype.append(False)
    else:
        target_weektype.append(True)
    if target_weektype[0]:
        target_weektype.append("ЗНАМЕНАТЕЛЬ")
    else:
        target_weektype.append("ЧИСЛИТЕЛЬ")
    user_id = callback.message.chat.id
    schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=target_weekday, week_type=target_weektype)

    weekdays = ("понедельник", "вторник", "среда", "четверг", "пятница", "суббота")
    weekday_name = weekdays[int(target_weekday) - 1]
    # converting needed weekday names (if weekday == 'среда', we want to write it as 'среду'
    # since that's the right spelling)
    if(weekday_name.endswith("а")):
        weekday_name = weekday_name[:-1] + "у"
    await callback.answer(text=f"Получаю расписание на {weekday_name}")

    await callback.message.answer(text=schedule, reply_markup=share_schedule.generate_keyboard(""))
    await callback.message.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                         reply_markup=await get_path_classes(schedule))


@dp.callback_query_handler(schedule_callback.filter(time="week"), state=RegistrationStates.RegistrationComplete)
async def show_week_schedule(callback: CallbackQuery, callback_data: dict):
    target_weektype = []
    
    if callback_data.get("week_type") == "1":
        target_weektype.append(False)
    else:
        target_weektype.append(True)
    if target_weektype[0]:
        target_weektype.append(f"ЗНАМЕНАТЕЛЬ")
    else:
        target_weektype.append("ЧИСЛИТЕЛЬ")
    await callback.answer(text="Получаю расписание на неделю")
    user_id = callback.message.chat.id
    week_schedules = await get_week_schedule_by_userid1(user_id=user_id, week_type=target_weektype)
    await callback.message.answer(text="Расписание на неделю:")
    for schedule in week_schedules:
        await callback.message.answer(text=schedule, reply_markup=share_schedule.generate_keyboard(""))



