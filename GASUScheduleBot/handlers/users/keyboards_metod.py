from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from loader import dp, storage
from aiogram.types.web_app_info import WebAppInfo
from filters.user_filter import IsUser
from filters import IsAdmin, IsModer
from aiogram.dispatcher import FSMContext
from utils.db_api.db_gino import db
from utils.db_api.models.user import User
from utils.db_api.models.schedule_group_type_day import ScheduleGroupLessonsNew, AcademicGroup

URL_FACULTY = [
                    ["строительный факультет", "Instagramm: https://instagram.com/sfgasu/", "ВКонтакте: https://vk.com/sfgasu"],
                    ["архитектурный факультет", "Instagramm: https://instagram.com/afgasu/", "ВКонтакте: https://vk.com/afgasu"],
                    ["факультет экономики и управления", "Instagramm: https://instagram.com/feu_spbgasu/", "ВКонтакте: https://vk.com/feu_spbgasu"],
                    ["факультет инженерной экологии и городского хозяйства", "Telegram: https://t.me/fieigh"],
                    ["автомобильно-дорожный факультет", "Instagramm: https://instagram.com/adf_spbgasu/", "ВКонтакте: https://vk.com/adf_gasu"],
                    ["факультет судебных экспертиз и права в строительстве и на транспорте", "Instagramm: https://instagram.com/fseipst_gasu/", "ВКонтакте: https://vk.com/fseipst"]
              ]

@dp.message_handler(IsUser(), state="*", content_types=types.ContentTypes.ANY)
async def get_text_messages(msg: types.Message):
    if msg.text == '🗓Расписание':
        await msg.answer('ℹ️Используйте следующие команды:\n\n📲 /today - Рассписание на сегодня'
                         '\n📲 /tomorrow - Расписание на завтра'
                         '\n📲 /week - Расписание на неделю'
                         '\n📲 /selectschedule - Выбор нужного расписания на любой день с помощью кнопок')

    elif msg.text == '🗺Карта СПбГАСУ':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Карта СПбГАСУ", web_app=WebAppInfo(url=f"https://map.spbgasu.ru")))
        await msg.answer(text=f"Посмотрите кабинеты на карте не выходя из Telegram!",
                             reply_markup=markup)


    elif msg.text == '🌐Полезные ссылки':
        from_chat_id = msg.from_user.id
        curr_user = await User.get(int(from_chat_id))
        faculty_name_qure = await db.select([db.func.distinct(AcademicGroup.faculty)]).where(
            AcademicGroup.name == curr_user.group).gino.all()
        faculty_name = list(map(lambda x: str(x[0]), faculty_name_qure))

        text_for_msg = ""
        for facult in URL_FACULTY:
            if facult[0] == faculty_name[0]:
                for cur_url in facult:
                    text_for_msg += cur_url + "\n\n"
                break


        await msg.answer(f'🌐Все соцсети для вашего факультета!🌐\n\n{text_for_msg}')

    else:
        await msg.answer(text=f"Я пониманию только специальные команды.\n"
                             f"Для справки нажми сюда - /help.")


