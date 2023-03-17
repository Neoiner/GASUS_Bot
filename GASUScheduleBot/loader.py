from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from utils.db_api.db_gino import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data import config
import redis

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage(config.REDIS_IP, 6379, db=1)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

__all__ = ["bot", "storage", "dp", "db", "scheduler"]

