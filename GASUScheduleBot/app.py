from aiogram import executor
from data.config import TIMEZONE
from loader import dp, scheduler
from utils.db_api import db_gino
from utils.scheduled_jobs import send_schedule_to_subscribed_users
from utils.set_bot_commands import set_default_commands
import aioredis
import middlewares, filters, handlers

from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # Настраиваем команды
    await set_default_commands(dp)

    # Добавляем задачу scheduler'у
    scheduler.add_job(send_schedule_to_subscribed_users, 'cron', hour='8-23', minute='*/30', timezone=TIMEZONE)

    # Копируем из

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
