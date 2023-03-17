from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp
from states.registration import RegistrationStates
from aiogram.utils.markdown import hbold

# handler for /help command, returns description of available commands
@dp.message_handler(CommandHelp(), state=RegistrationStates.RegistrationComplete)
async def bot_help(message: Message):
    text = (f"Инструкция к боту - bit.ly/2Q0pZv6\n",
            f"{hbold('Список команд: ')}",
            "/start - Запустить бота",
            "/help - Справка по командам",
            "/today - Расписание на сегодня",
            "/tomorrow - Расписание на завтра",
            "/week - Расписание на неделю",
            "/changegroup - Поменять группу",
            "/subscribe - Подписаться на рассылку расписания",
            "/selectschedule - Выбор расписания с помощью кнопок",
            "/differentgroupschedule - Расписание другой группы")
    
    await message.answer("\n".join(text))
