from loader import dp
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from states.different_group_search import DifferentGroupSearchStates
from states.registration import RegistrationStates
from utils.db_api.methods.schedule_methods import get_day_schedule_by_userid1, get_user_group, get_week_info
from utils.db_api.methods.schedule_methods import get_all_groups, get_day_schedule_by_groupname1
from utils import schedule_to_text, group_name
from keyboards.inline import back_to_inline_mode
from utils.db_api.models.schedule_group_type_day import ScheduleGroupTypeDay


#if user has no state, he's not registered -> send him to register
@dp.inline_handler(state=None)
async def send_user_to_register(query: InlineQuery):
    # cache time set to 0, otherwise bot mishandles empty queries
    await query.answer(results=[], switch_pm_text="Зарегистрироваться для использования бота",
                       switch_pm_parameter="connect_user_from_inline_mode", cache_time=0, is_personal=True)

#if user's registered and input field in inline mode is empty, show schedules for all days
@dp.inline_handler(text="", state=[RegistrationStates.RegistrationComplete, DifferentGroupSearchStates.GroupFound])
async def empty_query(query: InlineQuery):
    user_id = query.from_user.id
    user_group = await get_user_group(user_id=user_id)
    weekday_names = ("понедельник", "вторник", "среда", "четверг", "пятница", "суббота")
    all_days_schedules = []
    current_week_info = await get_week_info()
    next_week_info = await get_week_info(for_next_week=True)

    # schedules for current week
    for weekday in range(1, 7):
        weekday_schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=weekday)
        # converting needed weekday names (if weekday == 'среда', we want to write it as 'среду' since that's the right spelling)
        weekday_name = weekday_names[weekday - 1]
        weekday_formatted = weekday_name
        if (weekday_name.endswith("а")):
            weekday_formatted = weekday_name[:-1] + "у"
        all_days_schedules.append(InlineQueryResultArticle(
            id=f"{weekday_schedule.group_name_with_type_and_day}",
            title=f"{user_group} / {weekday_name} / ТЕКУЩАЯ",
            input_message_content=InputTextMessageContent(message_text=weekday_schedule),
            description=f"Расписание группы {user_group} на {weekday_formatted}, неделя - {current_week_info[1]}."
        ))

    # schedules for next week
    for weekday in range(1, 7):
        weekday_schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=weekday,
                                                                                  week_type=next_week_info[0])
        # converting needed weekday names (if weekday == 'среда', we want to write it as 'среду' since that's the right spelling)
        weekday_name = weekday_names[weekday - 1]
        weekday_formatted = weekday_name
        if (weekday_name.endswith("а")):
            weekday_formatted = weekday_formatted[:-1] + "у"
        all_days_schedules.append(InlineQueryResultArticle(
            title=f"{user_group} / {weekday_name} / {next_week_info[1]}",
            input_message_content=InputTextMessageContent(message_text=weekday_schedule),
            description=f"Расписание группы {user_group} на {weekday_formatted}, неделя - {next_week_info[1]}."
        ))
    #cache time set to 0, otherwise bot mishandles empty queries
    await query.answer(results=all_days_schedules, cache_time=0, is_personal=True)


# handles input to enable search for different group schedules
@dp.inline_handler(state=[RegistrationStates.RegistrationComplete, DifferentGroupSearchStates.GroupFound])
async def different_group_schedule_inline_search(query: InlineQuery):
    # get group_name by trimming whitespaces
    target_group_name = query.query.strip()
    target_group_simplified = await group_name.simplify(target_group_name)
    target_group = ''

    all_groups = await get_all_groups()
    group_found = False
    for group in all_groups:
        group_simplified = await group_name.simplify(group)
        if target_group_simplified == group_simplified:
            group_found = True
            target_group = group
            break


    if (group_found):
        weekday_names = ("понедельник", "вторник", "среда", "четверг", "пятница", "суббота")
        target_group_all_days_schedules = []
        current_week_info = await get_week_info()
        next_week_info = await get_week_info(for_next_week=True)

        # schedules for current week
        for weekday in range(1, 7):
            weekday_schedule: ScheduleGroupTypeDay = await get_day_schedule_by_groupname1(group_name=target_group, weekday=weekday)
            # converting needed weekday names (if weekday == 'среда', we want to write it as 'среду'
            # since that's the right spelling)
            weekday_name = weekday_names[weekday - 1]
            weekday_formatted = weekday_name
            if (weekday_name.endswith("а")):
                weekday_formatted = weekday_formatted[:-1] + "у"
            target_group_all_days_schedules.append(InlineQueryResultArticle(
                title=f"{target_group} / {weekday_name} / ТЕКУЩАЯ",
                input_message_content=InputTextMessageContent(message_text=weekday_schedule),
                description=f"Расписание группы {target_group} на {weekday_formatted}, неделя - {current_week_info[1]}."
            ))

        # schedules for next week
        for weekday in range(1, 7):
            weekday_schedule: ScheduleGroupTypeDay = await get_day_schedule_by_groupname1(group_name=target_group,
                                                                                         weekday=weekday, week_type=next_week_info[0])

            # converting needed weekday names (if weekday == 'среда', we want to write it as 'среду'
            # since that's the right spelling)
            weekday_name = weekday_names[weekday - 1]
            weekday_formatted = weekday_name
            if (weekday_name.endswith("а")):
                weekday_formatted = weekday_formatted[:-1] + "у"
            target_group_all_days_schedules.append(InlineQueryResultArticle(
                title=f"{target_group} / {weekday_name} / {next_week_info[1]}",
                input_message_content=InputTextMessageContent(message_text=weekday_schedule),
                description=f"Расписание группы {target_group} на {weekday_formatted}, неделя - {next_week_info[1]}."
            ))

        await query.answer(results=target_group_all_days_schedules, cache_time=60, is_personal=True)

    else:

        # cache time set to 0, otherwise bot mishandles empty queries
        await query.answer(results=[InlineQueryResultArticle(
                id=f"group_not_found",
                title=f"Группа {target_group_name} не найдена.",
                input_message_content=InputTextMessageContent(
                    message_text=f"Я не нашёл такую группу. Попробуй поискать другие группы?"),
                reply_markup=back_to_inline_mode.keyboard
        )], cache_time=0)











