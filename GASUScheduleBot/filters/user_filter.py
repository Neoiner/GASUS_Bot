from aiogram.types import Message
from aiogram.dispatcher.filters import Filter


class IsUser(Filter):

    async def check(self, message: Message) -> bool:
        return True if not message.from_user.is_bot else False


