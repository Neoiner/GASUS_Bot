from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Справка по командам"),
        types.BotCommand("today", "Расписание на сегодня"),
        types.BotCommand("tomorrow", "Расписание на завтра"),
        types.BotCommand("week", "Расписание на неделю"),
        types.BotCommand("selectschedule", "Выбор нужного расписания на любой день недели с помощью кнопок"),
        types.BotCommand("subscribe", "Подписаться на рассылку расписания"),
        types.BotCommand("changegroup", "Поменять группу"),
        types.BotCommand("differentgroupschedule", "Узнать расписание другой группы"),
        types.BotCommand("openmap", "Открыть карту СПбГАСУ"),
    ])
