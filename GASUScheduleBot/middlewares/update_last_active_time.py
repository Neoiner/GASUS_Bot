from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery
from utils.db_api.methods.user_methods import update_user_last_active_time


class UpdateUserLastActiveTimeMiddleware(BaseMiddleware):

    async def on_process_message(self, message: Message, data: dict):
        target_user_id = message.from_user.id
        await update_user_last_active_time(user_id=target_user_id)


    async def on_process_callback_query(self, callback: CallbackQuery, data: dict):
        target_user_id = callback.message.from_user.id
        await update_user_last_active_time(user_id=target_user_id)


    async def on_process_inline_query(self, query: InlineQuery, data: dict):
        target_user_id = query.from_user.id
        await update_user_last_active_time(user_id=target_user_id)



