from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic
from loader import dp
from states.registration import RegistrationStates
from utils.db_api.methods.user_methods import create_user
from utils.db_api.methods.schedule_methods import get_all_groups, get_available_faculties
from utils.db_api.models.user import User
from keyboards.inline import back_to_inline_mode
from utils import group_name


# handler to inform user that command are available only after registration
@dp.message_handler(regexp='(\/)\w+', state=[RegistrationStates.RegisterGroup, RegistrationStates.RegisterGroupFromInline])
async def remind_user_he_has_to_register(message: Message):
    await message.answer(text=f"Чтобы пользоваться командами,\n"
                              f"я должен сначала тебя зарегистрировать.\n\n"
                              f"Пожалуйста, напиши мне номер своей группы.\n"
                              f"Можешь писать заглавными/строчными {hbold('русскими')} буквами, '-' ставить {hbold('не обязательно')}.\n\n"
                              f"Например, я пойму {hitalic('любой')} из этих вариантов: 3а1, 3А1, 3-а-1.")


@dp.message_handler(state=[RegistrationStates.RegisterGroup, RegistrationStates.RegisterGroupFromInline])
async def register_group(message: Message, state: FSMContext):
    entered_group = message.text
    group_to_register = ''
    entered_group_simplified = await group_name.simplify(entered_group)
    current_state = await state.get_state()

    all_groups = await get_all_groups()
    group_found = False
    for group in all_groups:
        group_simplified = await group_name.simplify(group)
        if entered_group_simplified == group_simplified:
            group_found = True
            group_to_register = group
            break

    if(group_found):
        # if group found, create new user in db
        user = User()
        user.id = message.from_user.id
        user.first_name = message.from_user.first_name
        user.last_name = message.from_user.last_name
        user.username = message.from_user.username
        user.group = group_to_register
        user.daily_subscription_on = False
        user.weekly_subscription_on = False

        await create_user(user)
        # if user comes to registration from inline, send him message with button to inline mode
        if (current_state == "RegistrationStates:RegisterGroupFromInline"):
            await message.answer(text=f"Регистрация завершена!\n"
                                      f"Твоя группа - {hbold(group_to_register)}\n\n"
                                      f"Чтобы посмотреть расписание, напиши одну из команд:\n"
                                      f"расписание на {hitalic('сегодня')} - /today\n"
                                      f"расписание на {hitalic('завтра')} - /tomorrow\n"
                                      f"расписание на {hitalic('неделю')} - /week\n\n",
                                 reply_markup=back_to_inline_mode.keyboard)
        else:
            await message.answer(text=f"Регистрация завершена!\n"
                                      f"Твоя группа - {hbold(group_to_register)}\n\n"
                                      f"Справка по всем моим командам - /help\n\n"
                                      f"Чтобы посмотреть расписание, напиши одну из команд:\n"
                                      f"расписание на {hitalic('сегодня')} - /today\n"
                                      f"расписание на {hitalic('завтра')} - /tomorrow\n"
                                      f"расписание на {hitalic('неделю')} - /week\n\n"
                                      f"Ещё ты можешь отправить команду /selectschedule\n"
                                      f"для выбора расписания с помощью кнопок.")

        # finish registration process by setting RegistrationComplete state
        await RegistrationStates.RegistrationComplete.set()

    else:
        available_faculties = await get_available_faculties()
        bachelor_available_faculties = "\n".join(available_faculties)

        await message.answer(text=f"Не могу найти группу {hbold(entered_group)}...\n\n"
                                  f"Возможно, неправильно введено название группы, или "
                                  f"у меня нет расписания для твоего факультета?\n\n"
                                  f"Факультеты, для которых у меня есть расписание:\n\n"
                                  f"{hitalic(bachelor_available_faculties)}\n\n\n"
                                  f"Попробуй ещё раз.")




