from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
from aiogram.utils.markdown import hbold, hitalic
from filters import IsAdmin, IsModer
from loader import dp, storage
from utils.db_api.db_gino import db
from utils.db_api.models.schedule_group_type_day import ScheduleGroupLessonsNew, AcademicGroup
from states.NotifyModerator import NotifyModeratorStates
from states.NotifyFacultyOrGroup import NotifyFaculty_Group
from states.registration import RegistrationStates
from keyboards.inline.notification import cancel_notification_prompt, send_notification_prompt, cancel_survey_prompt, choose_type_of_notification, send_notification_moderator
from keyboards.inline.notification import survey, send_survey_prompt
from keyboards.callbackdatas.send_notification_callbackdata import send_notification_callback
from keyboards.callbackdatas.survey_callbackdata import survey_callback
from utils.db_api.methods.user_methods import get_all_user_ids
from utils.db_api.methods.schedule_methods import get_all_groups, get_available_faculties
from utils.db_api.models.user import User
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.callbackdatas.send_notification_callbackdata import send_notification_callback
from data.config import ADMINS

GLOBAL_FACULTY = "" #For saving Faculty
GLOBAL_CHOOSE = 0 #For saving moderator choose (Group or faculty)
GLOBAL_YEAR = 0 #For saving year
GLOBAL_GROUP = [] #this massive of notifying group

# Notifications for moders handlers


@dp.message_handler(IsModer(), Command("notifymoder", prefixes="!/"), state="*")
async def ask_for_notification_message(message: Message):
    await NotifyModeratorStates.ModeratorNotify.set()
    moder_id = message.from_user.id
    from_chat_id = moder_id
    message_id = message.message_id

    await message.answer(text=f'Выберете вариант рассылки:',
                         reply_markup=choose_type_of_notification.generate_keyboard(from_chat_id=from_chat_id, target_message_id=message_id))


@dp.callback_query_handler(IsModer(), text="for_faculty", state=NotifyModeratorStates.ModeratorNotify)
async def cancel_notification_setup(callback: CallbackQuery):

    await NotifyModeratorStates.Faculty.set()
    await callback.answer()
    available_faculties = await get_available_faculties()
    bachelor_available_faculties = "\n".join(available_faculties)
    await callback.message.edit_text(text=f"Введите факультет.\n\n\n"
                              f"Вот список факультетов:\n\n\n"
                              f"{hitalic(bachelor_available_faculties)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Строительный факультет", callback_data='SF')],
                                    [InlineKeyboardButton(text="Архитектурный факультет", callback_data='AF')],
                                    [InlineKeyboardButton(text="Факультет судебных экспертиз и права в строительстве и на транспорте", callback_data='FSEPST')],
                                    [InlineKeyboardButton(text="Факультет инженерной экологии и городского хозяйства", callback_data='FIEGH')],
                                    [InlineKeyboardButton(text="Факультет экономики и управления", callback_data='FEU')],
                                    [InlineKeyboardButton(text="Автомобильно-дорожный факультет", callback_data='ADF')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))

@dp.callback_query_handler(IsModer(), text="cancel_notification_setup", state=NotifyModeratorStates.Faculty)
async def cancel_notification_setup(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text="Настройка рассылки отменена.")
    await RegistrationStates.RegistrationComplete.set()
    GLOBAL_GROUP.clear()


@dp.callback_query_handler(IsModer(), state=NotifyModeratorStates.Faculty)
async def choose_faculty_setup(callback: CallbackQuery):

    global GLOBAL_FACULTY
    if(callback.data == "SF"):
        GLOBAL_FACULTY = "Строительный факультет"
    elif(callback.data=="AF"):
        GLOBAL_FACULTY = "Архитектурный факультет"
    elif (callback.data == "FSEPST"):
        GLOBAL_FACULTY = "Факультет судебных экспертиз и права в строительстве и на транспорте"
    elif (callback.data == "FIEGH"):
        GLOBAL_FACULTY = "Факультет инженерной экологии и городского хозяйства"
    elif (callback.data == "FEU"):
        GLOBAL_FACULTY = "Факультет экономики и управления"
    elif (callback.data == "ADF"):
        GLOBAL_FACULTY = "Автомобильно-дорожный факультет"
    await callback.message.edit_text(text=f"Вы ввели:\n"
                              f"{hitalic(GLOBAL_FACULTY)}", reply_markup=send_notification_moderator.generate_keyboard())
    await NotifyModeratorStates.ModeratorNotifyFaculty.set()
    global GLOBAL_CHOOSE
    GLOBAL_CHOOSE = 2
    await callback.answer()


@dp.callback_query_handler(IsModer(), lambda c: c.data == "for_group", state=NotifyModeratorStates.ModeratorNotify)
async def start_notification_setup(callback: CallbackQuery):
    await callback.answer()
    available_faculties = await get_available_faculties()
    bachelor_available_faculties = "\n".join(available_faculties)
    await callback.message.edit_text(text=f"Введите факультет.\n\n\n"
                              f"Вот список факультетов:\n\n\n"
                              f"{hitalic(bachelor_available_faculties)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Строительный факультет", callback_data='SF')],
                                    [InlineKeyboardButton(text="Архитектурный факультет", callback_data='AF')],
                                    [InlineKeyboardButton(text="Факультет судебных экспертиз и права в строительстве и на транспорте", callback_data='FSEPST')],
                                    [InlineKeyboardButton(text="Факультет инженерной экологии и городского хозяйства", callback_data='FIEGH')],
                                    [InlineKeyboardButton(text="Факультет экономики и управления", callback_data='FEU')],
                                    [InlineKeyboardButton(text="Автомобильно-дорожный факультет", callback_data='ADF')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))

    await NotifyFaculty_Group.Group.set()
    global GLOBAL_CHOOSE
    GLOBAL_CHOOSE = 1

@dp.callback_query_handler(IsModer(), lambda c: c.data == "another_faculty", state=NotifyModeratorStates.Group)
async def start_notification_setup(callback: CallbackQuery):
    await callback.answer()
    available_faculties = await get_available_faculties()
    bachelor_available_faculties = "\n".join(available_faculties)
    await callback.message.edit_text(text=f"Введите факультет.\n\n\n"
                              f"Вот список факультетов:\n\n\n"
                              f"{hitalic(bachelor_available_faculties)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Строительный факультет", callback_data='SF')],
                                    [InlineKeyboardButton(text="Архитектурный факультет", callback_data='AF')],
                                    [InlineKeyboardButton(text="Факультет судебных экспертиз и права в строительстве и на транспорте", callback_data='FSEPST')],
                                    [InlineKeyboardButton(text="Факультет инженерной экологии и городского хозяйства", callback_data='FIEGH')],
                                    [InlineKeyboardButton(text="Факультет экономики и управления", callback_data='FEU')],
                                    [InlineKeyboardButton(text="Автомобильно-дорожный факультет", callback_data='ADF')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))

    await NotifyFaculty_Group.Group.set()
    global GLOBAL_CHOOSE
    GLOBAL_CHOOSE = 1

@dp.callback_query_handler(IsModer(), state=NotifyFaculty_Group.Group)
async def choose_faculty_for_group_setup(callback: CallbackQuery):
    global GLOBAL_FACULTY
    if (callback.data == "SF"):
        GLOBAL_FACULTY = "строительный факультет"
    elif (callback.data == "AF"):
        GLOBAL_FACULTY = "архитектурный факультет"
    elif (callback.data == "FSEPST"):
        GLOBAL_FACULTY = "факультет судебных экспертиз и права в строительстве и на транспорте"
    elif (callback.data == "FIEGH"):
        GLOBAL_FACULTY = "факультет инженерной экологии и городского хозяйства"
    elif (callback.data == "FEU"):
        GLOBAL_FACULTY = "факультет экономики и управления"
    elif (callback.data == "ADF"):
        GLOBAL_FACULTY = "автомобильно-дорожный факультет"
    await callback.message.edit_text(text=f"Вы ввели:\n"
                                          f"{hitalic(GLOBAL_FACULTY)}")
    await callback.message.edit_text(text=f"Выберете год обучения.\n\n\n",
                                        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(text="1 курс", callback_data='1')],
                                        [InlineKeyboardButton(text="2 курс", callback_data='2')],
                                        [InlineKeyboardButton(text="3 курс", callback_data='3')],
                                        [InlineKeyboardButton(text="4 курс", callback_data='4')],
                                        [InlineKeyboardButton(text="Выбрать другой факультет", callback_data='another_faculty')],
                                        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                        ]))
    await NotifyModeratorStates.Group.set()

@dp.callback_query_handler(IsModer(),lambda c: c.data == "another_year" ,state=NotifyFaculty_Group.Continue)
async def choose_faculty_for_group_setup(callback: CallbackQuery):
    global GLOBAL_FACULTY
    if (callback.data == "SF"):
        GLOBAL_FACULTY = "строительный факультет"
    elif (callback.data == "AF"):
        GLOBAL_FACULTY = "архитектурный факультет"
    elif (callback.data == "FSEPST"):
        GLOBAL_FACULTY = "факультет судебных экспертиз и права в строительстве и на транспорте"
    elif (callback.data == "FIEGH"):
        GLOBAL_FACULTY = "факультет инженерной экологии и городского хозяйства"
    elif (callback.data == "FEU"):
        GLOBAL_FACULTY = "факультет экономики и управления"
    elif (callback.data == "ADF"):
        GLOBAL_FACULTY = "автомобильно-дорожный факультет"
    await callback.message.edit_text(text=f"Вы ввели:\n"
                                          f"{hitalic(GLOBAL_FACULTY)}")
    await callback.message.edit_text(text=f"Выберете год обучения.\n\n\n",
                                        reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(text="1 курс", callback_data='1')],
                                        [InlineKeyboardButton(text="2 курс", callback_data='2')],
                                        [InlineKeyboardButton(text="3 курс", callback_data='3')],
                                        [InlineKeyboardButton(text="4 курс", callback_data='4')],
                                        [InlineKeyboardButton(text="Выбрать другой факультет", callback_data='another_faculty')],
                                        [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                        ]))
    await NotifyModeratorStates.Group.set()


@dp.callback_query_handler(IsModer(),lambda c: c.data != "another_faculty" and c.data != "cancel_notification_setup", state=NotifyModeratorStates.Group) #starting add group
async def choose_year_for_group_setup(callback: CallbackQuery):
    global GLOBAL_YEAR
    global GLOBAL_FACULTY
    global GLOBAL_GROUP
    if (callback.data == "1"):
            GLOBAL_YEAR = 1
    elif (callback.data == "2"):
            GLOBAL_YEAR = 2
    elif (callback.data == "3"):
            GLOBAL_YEAR = 3
    elif (callback.data == "4"):
            GLOBAL_YEAR = 4
    await callback.message.edit_text(text=f"Вы ввели:\n"
                                              f"{hitalic(GLOBAL_YEAR)} курс {hitalic(str(GLOBAL_FACULTY))}")


    selected_group = await db.select([db.func.distinct(AcademicGroup.name)]) \
            .where(AcademicGroup.faculty == GLOBAL_FACULTY).gino.all()
    selected_group_list = list(map(lambda x: str(x[0]), selected_group))
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in selected_group_list:
            if(int(i[-1]) == GLOBAL_YEAR):
                markup.add(InlineKeyboardButton(i, callback_data=i))
    markup.add(InlineKeyboardButton("Закончить ввод", callback_data='stop'))
    markup.add(InlineKeyboardButton("Выбрать другой курс", callback_data='another_year'))
    markup.add(InlineKeyboardButton("Отменить рассылку", callback_data='cancel_notification_setup'))

    await callback.message.answer(text=f"Выберете группы\n\n\n", reply_markup=markup)
    await NotifyFaculty_Group.Continue.set()


@dp.callback_query_handler(IsModer(), state=NotifyFaculty_Group.ChangeFaculty)
async def change_faculty(callback: CallbackQuery):
    await callback.answer()
    available_faculties = await get_available_faculties()
    bachelor_available_faculties = "\n".join(available_faculties)
    await callback.message.edit_text(text=f"Введите факультет.\n\n\n"
                              f"Вот список факультетов:\n\n\n"
                              f"{hitalic(bachelor_available_faculties)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Строительный факультет", callback_data='SF')],
                                    [InlineKeyboardButton(text="Архитектурный факультет", callback_data='AF')],
                                    [InlineKeyboardButton(text="Факультет судебных экспертиз и права в строительстве и на транспорте", callback_data='FSEPST')],
                                    [InlineKeyboardButton(text="Факультет инженерной экологии и городского хозяйства", callback_data='FIEGH')],
                                    [InlineKeyboardButton(text="Факультет экономики и управления", callback_data='FEU')],
                                    [InlineKeyboardButton(text="Автомобильно-дорожный факультет", callback_data='ADF')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))

    await NotifyFaculty_Group.Group.set()
    global GLOBAL_CHOOSE
    GLOBAL_CHOOSE = 1


@dp.callback_query_handler(IsModer(), lambda c: c.data != "stop" and c.data != "delete_group",state=NotifyFaculty_Group.Continue) #Choose group for notify. You can exchange year and faculty here.
#This function work while Moderator adding some new group
async def choose_group(callback: CallbackQuery):
    global GLOBAL_YEAR
    global GLOBAL_FACULTY
    global GLOBAL_GROUP
    if(callback.data == "cancel_notification_setup"):
        await callback.answer()
        await callback.message.edit_text(text="Настройка рассылки отменена.")
        await RegistrationStates.RegistrationComplete.set()
        GLOBAL_GROUP.clear()
    else:
        if(callback.data != "continue"):
            GLOBAL_GROUP.append(callback.data)

        selected_group = await db.select([db.func.distinct(AcademicGroup.name)]) \
            .where(AcademicGroup.faculty == GLOBAL_FACULTY).gino.all()
        selected_group_list = list(map(lambda x: str(x[0]), selected_group))
        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        for i in selected_group_list:
            if (int(i[-1]) == GLOBAL_YEAR):
                markup.add(InlineKeyboardButton(i, callback_data=i))
        markup.add(InlineKeyboardButton("Закончить ввод", callback_data='stop'))
        markup.add(InlineKeyboardButton("Выбрать другой курс", callback_data='another_year'))
        markup.add(InlineKeyboardButton("Удалить группу", callback_data='delete_group'))
        markup.add(InlineKeyboardButton("Отменить рассылку", callback_data='cancel_notification_setup'))

        await callback.message.edit_text(text=f"Вы ввели {hitalic(GLOBAL_GROUP)}\n\n\n Выберете группы.\n\n\n",
                                      reply_markup=markup)
        await NotifyFaculty_Group.Continue.set()


@dp.callback_query_handler(IsModer(), lambda c: c.data == "delete_group", state=NotifyFaculty_Group.Continue)
async def delete_group(callback: CallbackQuery):
    global GLOBAL_GROUP
    markup = InlineKeyboardMarkup()
    for i in GLOBAL_GROUP:
        markup.add(InlineKeyboardButton(i, callback_data=i))

    await callback.message.edit_text(text=f"Выберете группу для удаления:\n\n\n",
                                     reply_markup=markup)

    await NotifyFaculty_Group.DeleteGroup.set()


@dp.callback_query_handler(IsModer(), state=NotifyFaculty_Group.DeleteGroup)
async def delete_group(callback: CallbackQuery):
    global GLOBAL_GROUP
    GLOBAL_GROUP.remove(callback.data)
    await callback.message.edit_text(text=f"Группа удалена.",
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                         [InlineKeyboardButton(text="Начать ввод сообщения",
                                                               callback_data='start_notification')],
                                         [InlineKeyboardButton(text="Продолжить ввод групп",
                                                               callback_data='continue')],
                                         [InlineKeyboardButton(text="Удалить еще",
                                                               callback_data='delete_group')],
                                         [InlineKeyboardButton(text="Отменить рассылку",
                                                               callback_data='cancel_notification_setup')]
                                     ]))
    await NotifyFaculty_Group.Continue.set()


@dp.callback_query_handler(IsModer(), lambda c: c.data == "stop", state=NotifyFaculty_Group.Continue)
async def check_group(callback: CallbackQuery):
    global GLOBAL_GROUP
    await callback.message.edit_text(text=f"Давай проверим группы:\n\n\n{hitalic(GLOBAL_GROUP)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Начать ввод сообщения", callback_data='start_notification')],
                                    [InlineKeyboardButton(text="Редактировать группы", callback_data='edit_group')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))
    await NotifyModeratorStates.ModeratorNotifyFaculty.set()


@dp.callback_query_handler(IsModer(), text="edit_group", state=NotifyModeratorStates.ModeratorNotifyFaculty)
async def choose_action(callback: CallbackQuery):
    await callback.message.edit_text(text=f"Что вы хотите сделать?\n\n\n{hitalic(GLOBAL_GROUP)}", reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="Удалить группу", callback_data='delete_group')],
                                    [InlineKeyboardButton(text="Добавить группу", callback_data='continue')],
                                    [InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_notification_setup')]
                                ]))
    await NotifyFaculty_Group.Continue.set()


@dp.callback_query_handler(IsModer(), text="start_notification", state=NotifyModeratorStates.ModeratorNotifyFaculty)
async def start_notification(callback: CallbackQuery):

    await callback.answer()
    await callback.message.answer(text=f'Присылай сообщение для рассылки, '
                                    f'я отправлю его копию всем зарегистрированным пользователям данного факультета.',
                                    reply_markup=cancel_notification_prompt.keyboard)


@dp.message_handler(IsModer(), state=NotifyModeratorStates.ModeratorNotifyFaculty, content_types=types.ContentType.ANY)
async def check_notification_message(message: Message):
    admin_id = message.from_user.id

    from_chat_id = admin_id
    message_id = message.message_id

    await message.answer(text="Давай проверим сообщение перед отправкой:")
    # In pm with bot, chat_id = user_id
    await message.copy_to(chat_id=admin_id,
                          reply_markup=send_notification_prompt.generate_keyboard(from_chat_id=from_chat_id,
                                                                                  target_message_id=message_id))

    global GLOBAL_CHOOSE
    if GLOBAL_CHOOSE == 1:
        await NotifyFaculty_Group.StartNotifyGroup.set()
    else:
        await NotifyFaculty_Group.Faculty.set()


@dp.callback_query_handler(IsModer(), text="cancel_notification_setup", state="*")
async def cancel_notification_setup(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Настройка рассылки отменена.")
    await RegistrationStates.RegistrationComplete.set()
    GLOBAL_GROUP.clear()


@dp.callback_query_handler(IsModer(), text="edit_notification", state=NotifyFaculty_Group.Faculty)
async def edit_notification(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Пришли новое сообщение для рассылки.")
    await NotifyModeratorStates.ModeratorNotifyFaculty.set()

@dp.callback_query_handler(IsModer(), send_notification_callback.filter(), state=NotifyFaculty_Group.Faculty)
async def send_notification_for_faculty(callback: CallbackQuery, callback_data: dict):
    await RegistrationStates.RegistrationComplete.set()
    global GLOBAL_FACULTY




    group_query = await db.select([db.func.distinct(AcademicGroup.name)]).where(AcademicGroup.faculty == GLOBAL_FACULTY).gino.all()
    group_list = list(map(lambda x: str(x[0]), group_query))



    from_chat_id = int(callback_data.get("from_chat_id"))
    target_message_id = int(callback_data.get("message_id"))


    for admin in ADMINS:
        try:
            existing_user = await User.get(int(from_chat_id))
            await dp.bot.send_message(admin,  text="Модератор @" + str(existing_user.username) + " ID: " + str(from_chat_id) + " начал рассылку сообщений ФАКУЛЬТЕТУ. " + GLOBAL_FACULTY)
            await dp.bot.copy_message(chat_id=admin, from_chat_id=from_chat_id, message_id=target_message_id)
        except:
            pass



    await callback.message.delete_reply_markup()

    all_users_ids = await get_all_user_ids()
    for user_id in all_users_ids:
        check_group_for_faculty = False
        existing_user = await User.get(int(user_id))
        if(existing_user == None):
            continue
        for group_cur in group_list:
            if existing_user.group == group_cur:
                check_group_for_faculty = True
        # In pm with bot, chat_id = user_id
        if check_group_for_faculty:
            try:
                await dp.bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=target_message_id)
                #await dp.bot.send_message(chat_id=from_chat_id, text=str(user_id) + "   " + existing_user.group)
            except:
                pass
    GLOBAL_GROUP.clear()
    await dp.bot.send_message(chat_id=from_chat_id, text="Рассылка успешно завершена!")



@dp.callback_query_handler(IsModer(), send_notification_callback.filter(), state=NotifyFaculty_Group.StartNotifyGroup)
async def send_notification_for_faculty(callback: CallbackQuery, callback_data: dict):
    await RegistrationStates.RegistrationComplete.set()
    global GLOBAL_GROUP

    from_chat_id = int(callback_data.get("from_chat_id"))
    target_message_id = int(callback_data.get("message_id"))

    for admin in ADMINS:
        try:
            existing_user = await User.get(int(from_chat_id))
            await dp.bot.send_message(admin,  text="Модератор @" + str(existing_user.username) + " ID: " + str(from_chat_id) + " начал рассылку сообщений ГРУППАМ.\n\n\n" + str(GLOBAL_GROUP))
            await dp.bot.copy_message(chat_id=admin, from_chat_id=from_chat_id, message_id=target_message_id)
        except:
            pass

    await callback.message.delete_reply_markup()

    all_users_ids = await get_all_user_ids()
    for user_id in all_users_ids:
        check_group_for_faculty = False
        existing_user = await User.get(int(user_id))
        if(existing_user == None):
            continue
        for group_cur in GLOBAL_GROUP:
            if existing_user.group == group_cur:
                check_group_for_faculty = True
        # In pm with bot, chat_id = user_id
        if check_group_for_faculty:
            try:
                await dp.bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=target_message_id)
                #await dp.bot.send_message(chat_id=from_chat_id, text=str(user_id) + "   " + existing_user.group)
            except:
                pass
    GLOBAL_GROUP.clear()
    await dp.bot.send_message(chat_id=from_chat_id, text="Рассылка успешно завершена!")

