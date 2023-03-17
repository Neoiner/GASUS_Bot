import datetime

from aiogram import Dispatcher

from data.config import TIMEZONE
from keyboards.inline import share_schedule
from loader import dp, storage

from utils.db_api.methods.schedule_methods import get_day_schedule_by_userid1, get_week_info, get_week_schedule_by_userid1
from utils.db_api.methods.user_methods import get_subscribed_users_ids


async def send_schedule_to_subscribed_users():
    
    # get list of subscribed users
    subscribed_users_ids = await get_subscribed_users_ids()



    # get their subscription preferences
    for user_id in subscribed_users_ids:
        user_data = await storage.get_data(user=user_id)
        subscription_data = user_data.get('subscription_preferences')

        
        # safety check
        if subscription_data is not None:
            subscription_type = subscription_data.get('type')
            subscription_subtype = subscription_data.get('subtype')
            subscription_time = subscription_data.get('time')
            subscription_group = subscription_data.get('group')
            print(subscription_type, subscription_subtype, subscription_time, subscription_group)
            # check if user's target time matches current time
            now = datetime.datetime.now(tz=TIMEZONE)

            current_hour = now.hour
            # since we have only 2 options of 00 and 30 minutes in subscription, we round current minutes
            # to either 0 or 30 (cause scheduled job may run for some time and current time is 9:05)
            current_minute = 0 if now.minute < 30 else 30
            # weekday is 0-6, we make it 1-7
            current_weekday = now.weekday() + 1

            # time in subscription preferences is written like '9-30'
            # we get hour and minute by splitting and converting to int
            #await dp.bot.send_message(425163498, text=f"id: {user_id}\ntime: {subscription_time}")
            if(subscription_time != "none"):
                target_hour = int(subscription_time.split("-")[0])
                target_minute = int(subscription_time.split("-")[1])
            else:
                continue
            if current_hour == target_hour:
                if current_minute == target_minute:
                    # daily
                    if subscription_type == 'daily':
                        # if subscribed for next day schedule, skip message on saturday
                        if (subscription_subtype == 'next') and (current_weekday != 6):
                            tomorrow = now + datetime.timedelta(days=1)
                            tomorrow_weekday = tomorrow.weekday() + 1

                            schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=tomorrow_weekday)
                            await dp.bot.send_message(chat_id=user_id, text=f"Расписание на завтра:\n{schedule}",
                                                      reply_markup=share_schedule.generate_keyboard(""))

                        # if subscribed for current day schedule, skip message on sunday
                        elif (subscription_subtype == 'current') and (current_weekday != 7):
                            schedule = await get_day_schedule_by_userid1(user_id=user_id, weekday=current_weekday)
                            await dp.bot.send_message(chat_id=user_id, text=f"Расписание на сегодня:\n{schedule}")

                    # weekly
                    elif subscription_type == 'weekly':
                        if (subscription_subtype == 'sunday') and (current_weekday == 7):
                            next_week_info = await get_week_info(for_next_week=True)
                            await dp.bot.send_message(chat_id=user_id,
                                                      text=f"Расписание на следующую неделю: {next_week_info[1]}")

                            week_schedules = await get_week_schedule_by_userid1(user_id=user_id,
                                                                               week_type=next_week_info[0])
                            for schedule in week_schedules:

                                await dp.bot.send_message(chat_id=user_id, text=schedule)

                        elif (subscription_subtype == 'monday') and (current_weekday == 1):
                            current_week_info = await get_week_info()
                            await dp.bot.send_message(chat_id=user_id,
                                                      text=f"Расписание на текущую неделю: {current_week_info[1]}")

                            week_schedules = await get_week_schedule_by_userid1(user_id=user_id)
                            for schedule in week_schedules:
                                
                                await dp.bot.send_message(chat_id=user_id, text=schedule)

