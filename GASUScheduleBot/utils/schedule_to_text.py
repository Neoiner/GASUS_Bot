from aiogram.utils.markdown import hbold, hitalic
from utils.db_api.models.schedule_group_type_day import ScheduleGroupLessonsNew

async def convert(schedule, groupname, day_of_week, weektype):
    lectures_info = []
    day_of_week_simbol = dict()
    lecture_time_simbol = dict()
    day_of_week_simbol[1] = 'Понедельник'
    day_of_week_simbol[2] = 'Вторник'
    day_of_week_simbol[3] = 'Среда'
    day_of_week_simbol[4] = 'Четверг'
    day_of_week_simbol[5] = 'Пятница'
    day_of_week_simbol[6] = 'Суббота'
    
    lecture_time_simbol[1] = '09:00-10:30'
    lecture_time_simbol[2] = '10:45-12:15'
    lecture_time_simbol[3] = '12:30-14:00'
    lecture_time_simbol[4] = '15:00-16:30'
    lecture_time_simbol[5] = '16:45-18:15'
    lecture_time_simbol[6] = '18:30-20:00'
    lecture_time_simbol[7] = '20:15-21:45'
    
    
    is_day_off = True
    text_schedule = hbold(f"Группа {groupname}, {day_of_week_simbol[day_of_week]}\nНеделя {weektype}\n")
    if schedule:
        for oneless in schedule:
            text_schedule += hitalic(f"\n\n{lecture_time_simbol[oneless[1]]}\n")
            text_schedule += hbold(f"{oneless[0]} ({oneless[4]})")
            text_schedule += f"\nАудитория: "
            text_schedule += hitalic(f"{oneless[2]}\n")
            text_schedule += f"Преподаватель: "
            text_schedule += hitalic(f"{oneless[3]}")
    else:
        text_schedule += f"\nЗанятий нет!"
    
    return text_schedule
