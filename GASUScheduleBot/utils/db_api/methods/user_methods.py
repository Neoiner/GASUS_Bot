from utils.db_api.db_gino import db
from utils.db_api.models.user import User
from loader import storage
import redis
from data import config

async def create_user(user: User):
    existing_user = await User.get(user.id)
    if (existing_user is None):
        await user.create()


async def update_user_last_active_time(user_id):
    existing_user = await User.get(user_id)
    # update last active time only if user exists in db
    if (existing_user != None):
        await existing_user.update(last_active_time=db.func.now()).apply()


async def set_user_subscription_status_active(user_id, subscription_type):
    existing_user = await User.get(user_id)
    # update only if user exists in db
    # this method can be called only after registration, but
    # we're checking that user exists just in case
    if (existing_user != None):
        if subscription_type == "daily":
            await existing_user.update(daily_subscription_on=True).apply()
        elif subscription_type == "weekly":
            await existing_user.update(weekly_subscription_on=True).apply()


async def set_user_subscription_status_off(user_id):
    existing_user = await User.get(user_id)
    # update only if user exists in db
    # this method can be called only after registration, but
    # we're checking that user exists just in case
    if (existing_user != None):
        await existing_user.update(daily_subscription_on=False, weekly_subscription_on=False).apply()


async def get_user_group(user_id):

    target_group = await User.select('group').where(User.id == user_id).gino.scalar()

    return target_group


async def get_all_user_ids():
    #Find user in Redis
    query_all_users_ids = []
    r = redis.Redis(config.REDIS_IP, 6379, db=1)
    for key in r.scan_iter():
        query_all_users_ids.append((key.decode("utf-8").split(':')[2]))
        
    return query_all_users_ids
    #all_users_ids = list(map(lambda x: x[0], query_all_users_ids)) #If query_all_users_ids doesn`t work
    #return all_users_ids


async def get_subscribed_users_ids():
    query_result_users_ids = await User.select('id').where((User.daily_subscription_on == True) |
                                                           (User.weekly_subscription_on == True)).gino.all()

    subscribed_users_ids = list(map(lambda x: x[0], query_result_users_ids))
    return subscribed_users_ids



