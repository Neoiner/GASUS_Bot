from aiogram.types import Message
from aiogram.dispatcher.filters import Filter
from data.config import ADMINS
from utils.db_api.models.user import User

class IsAdmin(Filter):

    async def check(self, message: Message) -> bool:
        return message.from_user.id in list(map(lambda x: int(x), ADMINS))

class IsModer(Filter):

    async def check(self, message: Message) -> bool:
        checking_user = await User.select('is_moderator').where(User.id == message.from_user.id).gino.scalar()
        return checking_user



