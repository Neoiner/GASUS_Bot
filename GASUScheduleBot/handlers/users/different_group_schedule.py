import datetime

from aiogram.types import Message, CallbackQuery

from data.config import TIMEZONE
from loader import dp
from aiogram.utils.markdown import hbold, hitalic
from states.registration import RegistrationStates
from states.different_group_search import DifferentGroupSearchStates
from aiogram.dispatcher.filters.builtin import Command
from utils import schedule_to_text, group_name
from utils.db_api.methods.schedule_methods import get_all_groups, get_day_schedule_by_groupname1, \
    get_week_schedule_by_groupname1, get_available_faculties
from keyboards.callbackdatas.different_group_schedule_callbackdata import diffgroup_schedule_callback
from keyboards.inline.different_group import prompt_after_getting_diffgroup_schedule, cancel_different_group_search, \
    different_group_schedule_selection
from keyboards.callbackdatas.redirect_to_diffgroup_schedule_selection_callbackdata import redirect_to_schedule_selection_callback

@dp.message_handler(Command("differentgroupschedule"), state=RegistrationStates.RegistrationComplete)
async def show_different_group_search_prompt(message: Message):
    await DifferentGroupSearchStates.FindGroup.set()
    await message.answer(text=f"Пожалуйста, напиши мне номер группы, для которой ты "
                              f"хочешь узнать расписание.\n"
                              f"Номер группы можно писать без - и в любом регистре.\n\n"
                              f"Например, вот так {hitalic('1дасм1')} или так {hitalic('1ДАСМ1')}",
                         reply_markup=cancel_different_group_search.keyboard)



@dp.callback_query_handler(text="abort_different_group_search", state=DifferentGroupSearchStates)
async def cancel_search(callback: CallbackQuery):
    await RegistrationStates.RegistrationComplete.set()
    await callback.answer(text="Вы отменили поиск расписания другой группы.", show_alert=True)




@dp.message_handler(regexp='(\/)\w+', state=DifferentGroupSearchStates.FindGroup)
async def remind_user_to_cancel_search(message: Message):
    await message.answer(text=f"Похоже, ты хочешь использовать одну из моих команд.\n"
                              f"Эти команды работают только для {hbold('твоей')} группы.\n"
                              f"Для использования команды нужно завершить/отменить поиск.\n\n"
                              f"Для отмены поиска расписания другой группы, "
                              f"пожалуйста, нажми на кнопку ниже.\n\n"
                              f"Если хочешь посмотреть расписание другой группы, то "
                              f"напиши мне её номер.",
                         reply_markup=cancel_different_group_search.keyboard)


@dp.message_handler(state=DifferentGroupSearchStates.GroupFound)
async def inform_about_unexpected_input(message: Message):
    await message.answer(text=f"Пожалуйста, отмени поиск, чтобы я корректно работал.\n\n"
                              f"Для отмены поиска расписания другой группы, "
                              f"пожалуйста, нажми на кнопку ниже.\n\n",
                         reply_markup=cancel_different_group_search.keyboard)



@dp.message_handler(state=DifferentGroupSearchStates.FindGroup)
async def find_different_group(message: Message):
    entered_group = message.text
    target_group = ''
    entered_group_simplified = await group_name.simplify(entered_group)

    all_groups = await get_all_groups()
    group_found = False
    for group in all_groups:
        group_simplified = await group_name.simplify(group)
        if entered_group_simplified == group_simplified:
            group_found = True
            target_group = group
            break

    if (group_found):
        await DifferentGroupSearchStates.GroupFound.set()

        await message.answer(text=f"Группа {hbold(target_group)} найдена!\n\n"
                                  f"Выбери, какое расписание посмотреть:",
                             reply_markup=different_group_schedule_selection.generate_keyboard(target_group))

    else:
        available_faculties = await get_available_faculties()
        bachelor_available_faculties = "\n".join(available_faculties)


        await message.answer(text=f"Не могу найти группу {hbold(entered_group)}...\n\n"
                                  f"Возможно, неправильно введено название группы, или "
                                  f"у меня нет расписания для твоего факультета?\n\n"
                                  f"Факультеты, для которых у меня есть расписание:\n\n"
                                  f"{hitalic(bachelor_available_faculties)}\n\n\n"
                                  f"Попробуй ещё раз или отмени поиск.",
                             reply_markup=cancel_different_group_search.keyboard)



@dp.callback_query_handler(diffgroup_schedule_callback.filter(is_weekday="False", time="today"), state=DifferentGroupSearchStates.GroupFound)
async def show_diffgroup_today_schedule(callback: CallbackQuery, callback_data: dict):
    target_group_name = callback_data.get("group")
    await callback.answer(text=f"Получаю расписание группы {target_group_name}")

    # weekday is number 0-6(monday-sunday), we increment it, so it is 1-7
    now = datetime.datetime.now(TIMEZONE)
    weekday = now.weekday() + 1
    if (weekday == 7):
        await callback.message.answer(text="Сегодня воскресенье, занятий нет!\n"
                                           "Хороших выходных!")
    else:
        schedule = await get_day_schedule_by_groupname1(group_name=target_group_name, weekday=weekday)
        await callback.message.answer(text="Расписание на сегодня:")
        await callback.message.answer(text=schedule,
                                      reply_markup=prompt_after_getting_diffgroup_schedule.generate_keyboard(target_group_name))



@dp.callback_query_handler(diffgroup_schedule_callback.filter(is_weekday="False", time="tomorrow"), state=DifferentGroupSearchStates.GroupFound)
async def show_diffgroup_tomorrow_schedule(callback: CallbackQuery, callback_data: dict):
    target_group_name = callback_data.get("group")
    await callback.answer(text=f"Получаю расписание группы {target_group_name}")

    # weekday is number 0-6(monday-sunday), we increment it, so it is 1-7
    now = datetime.datetime.now(TIMEZONE)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_weekday = tomorrow.weekday() + 1
    if (tomorrow_weekday == 7):
        await callback.message.answer(text="Завтра воскресенье, занятий нет!\n"
                                           "Хороших выходных!")
    else:
        schedule = await get_day_schedule_by_groupname1(group_name=target_group_name, weekday=tomorrow_weekday)
        await callback.message.answer(text="Расписание на завтра:")
        await callback.message.answer(text=schedule,
                                      reply_markup=prompt_after_getting_diffgroup_schedule.generate_keyboard(target_group_name))



@dp.callback_query_handler(diffgroup_schedule_callback.filter(is_weekday="True"), state=DifferentGroupSearchStates.GroupFound)
async def show_diffgroup_weekday_schedule(callback: CallbackQuery, callback_data: dict):
    target_group_name = callback_data.get("group")
    target_weektype = []
    target_weektype.append(callback_data.get("week_type"))
    if target_weektype[0]:
        target_weektype.append("ЧИСЛИТЕЛЬ")
    else:
        target_weektype.append("ЗНАМЕНАТЕЛЬ")
    target_weekday = int(callback_data.get("weekday"))
    await callback.answer(text=f"Получаю расписание группы {target_group_name}")
    schedule = await get_day_schedule_by_groupname1(group_name=target_group_name, weekday=target_weekday, week_type=target_weektype)
    await callback.message.answer(text=schedule,
                                  reply_markup=prompt_after_getting_diffgroup_schedule.generate_keyboard(target_group_name))



@dp.callback_query_handler(diffgroup_schedule_callback.filter(is_weekday="False", time="week"), state=DifferentGroupSearchStates.GroupFound)
async def show_diffgroup_week_schedule(callback: CallbackQuery, callback_data: dict):
    target_group_name = callback_data.get("group")
    target_weektype = []
    target_weektype.append(callback_data.get("week_type"))
    if target_weektype[0]:
        target_weektype.append("ЧИСЛИТЕЛЬ")
    else:
        target_weektype.append("ЗНАМЕНАТЕЛЬ")
    await callback.answer(text=f"Получаю расписание группы {target_group_name}")
    week_schedules = await get_week_schedule_by_groupname1(group_name=target_group_name, week_type=target_weektype)
    await callback.message.answer(text="Расписание на неделю:")
    for schedule in week_schedules:
        await callback.message.answer(text=schedule,
                                      reply_markup=prompt_after_getting_diffgroup_schedule.generate_keyboard(target_group_name))



@dp.callback_query_handler(redirect_to_schedule_selection_callback.filter(), state=DifferentGroupSearchStates.GroupFound)
async def show_diffgroup_schedule_selection(callback: CallbackQuery, callback_data: dict):
    await callback.answer("Перенаправляю вас на выбор расписания")
    target_group_name = callback_data.get("group_name")
    await callback.message.answer(text=f"Выбери нужное расписание группы {hbold(target_group_name)}:",
                                  reply_markup=different_group_schedule_selection.generate_keyboard(target_group_name))










