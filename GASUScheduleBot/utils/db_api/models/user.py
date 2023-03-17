from sqlalchemy import Column, BigInteger, String, Boolean
from ..db_gino import db

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50))
    group = Column(String(15))
    daily_subscription_on = Column(Boolean())
    weekly_subscription_on = Column(Boolean())
    is_moderator = Column(Boolean())




