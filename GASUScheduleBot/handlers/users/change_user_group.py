from loader import dp
from aiogram.types import Message, CallbackQuery
from states.registration import RegistrationStates
from aiogram.dispatcher.filters.builtin import Command
from keyboards.inline import change_group_prompt
from utils import group_name
from utils.db_api.methods.schedule_methods import get_all_groups, get_available_faculties
from utils.db_api.models.user import User
from aiogram.utils.markdown import hbold, hitalic


# handler for /changegroup command, prompts user to change group
@dp.message_handler(Command("changegroup"), state=RegistrationStates.RegistrationComplete)
async def change_group(message: Message):

    await message.answer(text=f"Эта команда изменяет твою группу!\n\n"
                              f"Команда вызвана случайно? Не страшно, "
                              f"я пока ещё ничего не удалил. Чтобы {hbold('ОТМЕНИТЬ')} "
                              f"процесс смены группы - просто нажми кнопку нет.\n\n"
                              f"Если ты действительно хочешь поменять свою группу, то "
                              f"нажми кнопку да.\n\n"
                              f"{hitalic('Меняем твою группу?')}",
                         reply_markup=change_group_prompt.keyboard)


# handler for /changegroup command, prompts user to change group
@dp.callback_query_handler(text="abort_change_group", state=RegistrationStates.RegistrationComplete)
async def cancel_group_change(callback: CallbackQuery):
    await callback.answer(text="Вы отменили смену группы.")


@dp.callback_query_handler(text="proceed_change_group", state=RegistrationStates.RegistrationComplete)
async def proceed_group_change(callback: CallbackQuery):
    await callback.answer(text="Вы запустили смену группы.")

    await RegistrationStates.ChangeGroup.set()
    await callback.message.answer(text=f"Пожалуйста, напиши мне новый номер группы:")



@dp.message_handler(state=RegistrationStates.ChangeGroup)
async def register_new_group(message: Message):
    entered_group = message.text
    group_to_update = ''
    entered_group_simplified = await group_name.simplify(entered_group)
    user_id = message.from_user.id

    all_groups = await get_all_groups()
    group_found = False
    for group in all_groups:
        group_simplified = await group_name.simplify(group)
        if entered_group_simplified == group_simplified:
            group_found = True
            group_to_update = group
            break

    if(group_found):
        await RegistrationStates.RegistrationComplete.set()

        # if group found, update existing user in db, after changing user's state
        existing_user = await User.get(user_id)
        await existing_user.update(group=group_to_update).apply()

        await message.answer(text=f"Регистрация завершена!\n"
                             f"Твоя {hitalic('новая')} группа - {hbold(group_to_update)}\n"
                             f"Чтобы посмотреть расписание, напиши одну из команд:\n"
                             f"расписание на {hitalic('сегодня')} - /today\n"
                             f"расписание на {hitalic('завтра')} - /tomorrow\n"
                             f"расписание на {hitalic('неделю')} - /week\n\n"
                             f"Ещё ты можешь отправить команду /selectschedule\n"
                             f"для выбора расписания с помощью кнопок.")

    else:
        available_faculties = await get_available_faculties()
        bachelor_available_faculties = "\n".join(available_faculties)


        await message.answer(text=f"Не могу найти группу {hbold(entered_group)}...\n\n"
                                  f"Возможно, неправильно введено название группы, или "
                                  f"у меня нет расписания для твоего факультета?\n\n"
                                  f"Факультеты, для которых у меня есть расписание:\n\n"
                                  f"{hitalic(bachelor_available_faculties)}\n\n\n"
                                  
                                  f"Попробуй ещё раз.")
