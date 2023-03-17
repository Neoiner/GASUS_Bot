import datetime

from data.config import TIMEZONE

from utils.db_api.db_gino import db
from utils.db_api.models.schedule_group_type_day import ScheduleGroupTypeDay
from utils.db_api.methods.user_methods import get_user_group
from utils.db_api.models.schedule_group_type_day import ScheduleGroupLessonsNew, AcademicGroup
from utils import schedule_to_text


async def get_available_faculties():
    
    all_faculties_query = await db.select([db.func.distinct(AcademicGroup.faculty)]).gino.all()
    all_faculties = list(map(lambda x: str(x[0]), all_faculties_query))

    return all_faculties


async def get_week_info(for_next_week = False):
    now = datetime.datetime.now(TIMEZONE)
    week_number = now.isocalendar()[1]

    if for_next_week:
        next_week = now + datetime.timedelta(weeks=1)
        week_number = next_week.isocalendar()[1]

    if (week_number % 2 == 0):
        week_info = [1, "ЗНАМЕНАТЕЛЬ"]
    else:
        week_info = [0, "ЧИСЛИТЕЛЬ"]
    return week_info


# For new db
async def get_day_schedule_by_userid1(user_id, weekday, week_type=None):
    week_text = ""
    if week_type == None:
        week_info = await get_week_info()
        week_types = week_info[0]
        week_text = week_info[1]
    else:
        week_types = week_type[0]
        week_text = week_type[1]
    if week_types == 0:
        week_bool = False
    else:
        week_bool = True
    print(week_types, week_text)
    user_group = await get_user_group(user_id)

    schedule_for_day = await db.select([ScheduleGroupLessonsNew.discipline, ScheduleGroupLessonsNew.number_of_less, ScheduleGroupLessonsNew.classroom, ScheduleGroupLessonsNew.professor, ScheduleGroupLessonsNew.format])\
        .where(ScheduleGroupLessonsNew.group_name == user_group)\
        .where(ScheduleGroupLessonsNew.day_of_week == weekday)\
        .where(ScheduleGroupLessonsNew.week == week_bool).gino.all()

    schedule_text = await schedule_to_text.convert(schedule_for_day, user_group, weekday, week_text)

    return schedule_text
    

async def get_day_schedule_by_groupname1(group_name, weekday, week_type=None):
    week_text = ""
    if week_type == None:
        week_info = await get_week_info()
        week_types = week_info[0]
        week_text = week_info[1]
    else:
        week_types = week_type[0]
        week_text = week_type[1]
    if week_types == 0:
        week_bool = False
    else:
        week_bool = True

    schedule_for_day = await db.select(
        [ScheduleGroupLessonsNew.discipline, ScheduleGroupLessonsNew.number_of_less, ScheduleGroupLessonsNew.classroom,
         ScheduleGroupLessonsNew.professor, ScheduleGroupLessonsNew.format]) \
        .where(ScheduleGroupLessonsNew.group_name == group_name) \
        .where(ScheduleGroupLessonsNew.day_of_week == weekday) \
        .where(ScheduleGroupLessonsNew.week == week_bool).gino.all()

    schedule_text = await schedule_to_text.convert(schedule_for_day, group_name, weekday, week_text)
    
    return schedule_text

async def get_week_schedule_by_userid1(user_id, week_type=None):
    # if function is invoked without week_type param, it defaults to None
    # and we get current week type
    week_text = ""
    if week_type == None:
        week_info = await get_week_info()
        week_types = week_info[0]
        week_text = week_info[1]
    else:
        week_types = week_type[0]
        week_text = week_type[1]
    if week_types == 0:
        week_bool = False
    else:
        week_bool = True

    user_group = await get_user_group(user_id)
    schedule_list = []
    for day_index in range(1, 7):
        schedule_for_day = await db.select(
            [ScheduleGroupLessonsNew.discipline, ScheduleGroupLessonsNew.number_of_less,
             ScheduleGroupLessonsNew.classroom,
             ScheduleGroupLessonsNew.professor, ScheduleGroupLessonsNew.format]) \
            .where(ScheduleGroupLessonsNew.group_name == user_group) \
            .where(ScheduleGroupLessonsNew.day_of_week == day_index) \
            .where(ScheduleGroupLessonsNew.week == week_bool).gino.all()

        schedule_text = await schedule_to_text.convert(schedule_for_day, user_group, day_index, week_text)
        schedule_list.append(schedule_text)
    return schedule_list


async def get_week_schedule_by_groupname1(group_name, week_type=None):
    # if function is invoked without week_type param, it defaults to None
    # and we get current week type
    week_text = ""
    if week_type == None:
        week_info = await get_week_info()
        week_types = week_info[0]
        week_text = week_info[1]
    else:
        week_types = week_type[0]
        week_text = week_type[1]
    if week_types == 0:
        week_bool = False
    else:
        week_bool = True

    schedule_list = []
    for day_index in range(1, 7):
        schedule_for_day = await db.select(
            [ScheduleGroupLessonsNew.discipline, ScheduleGroupLessonsNew.number_of_less,
             ScheduleGroupLessonsNew.classroom,
             ScheduleGroupLessonsNew.professor, ScheduleGroupLessonsNew.format]) \
            .where(ScheduleGroupLessonsNew.group_name == group_name) \
            .where(ScheduleGroupLessonsNew.day_of_week == day_index) \
            .where(ScheduleGroupLessonsNew.week == week_bool).gino.all()

        schedule_text = await schedule_to_text.convert(schedule_for_day, group_name, day_index, week_text)
        schedule_list.append(schedule_text)
    return schedule_list


async def get_all_groups():
    #get "group_name" unique db entries, put in list
    query_result_list = await db.select([db.func.distinct(AcademicGroup.name)]).gino.all()
    all_groups = list(map(lambda x: x[0], query_result_list))
    return all_groups
