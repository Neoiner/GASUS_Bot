from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
from utils.db_api.methods.user_methods import create_user
from filters import IsAdmin
from loader import dp, storage
from utils.db_api.models.user import User
from states.addmoderator import AddModeratorStates
from states.registration import RegistrationStates
from keyboards.inline.add_Moders import cancel_modersID_prompt, IDmoderator_prompt
from utils.db_api.methods.user_methods import get_all_user_ids
from keyboards.callbackdatas.addmoderator_callbackdata import send_addmoderator_callback

GLOBAL_MODERATOR_ID = 0

#For registrate moderator
@dp.message_handler(IsAdmin(), Command("addmoderator", prefixes="!/"), state="*")
async def ask_for_modersID_message(message: Message):
    await AddModeratorStates.SetupID.set()

    await message.answer(text=f'Введи ID пользователя TG, '
                              f'я проверю, зарегистрирован ли он, и можем ли мы добавить его в модераторы.',
                         reply_markup=cancel_modersID_prompt.keyboard)

@dp.callback_query_handler(IsAdmin(), text="cancel_moderatorID_setup", state=AddModeratorStates.SetupID)
async def cancel_moderatorID_setup(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Добавление модератора отменена.")
    await RegistrationStates.RegistrationComplete.set()


@dp.message_handler(IsAdmin(), state=AddModeratorStates.SetupID, content_types=types.ContentType.ANY)
async def check_notification_message(message: Message):
    admin_id = message.from_user.id
    global GLOBAL_MODERATOR_ID
    from_chat_id = admin_id
    message_id = message.message_id
    GLOBAL_MODERATOR_ID = int(message.text)
    #await message.answer(text="Проверь ID: " + message.text)
    await message.answer(text="Проверь ID: ")
    # In pm with bot, chat_id = user_id
    await message.copy_to(chat_id=admin_id,
                          reply_markup=IDmoderator_prompt.generate_keyboard(from_chat_id=from_chat_id,
                                                                                  target_message_id=message_id))


@dp.callback_query_handler(IsAdmin(), text="edit_moderator", state=AddModeratorStates.SetupID)
async def edit_notification(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Введите верный ID.")


@dp.callback_query_handler(IsAdmin(), send_addmoderator_callback.filter(), state=AddModeratorStates.SetupID)
async def check_modersID_message(callback: CallbackQuery, callback_data: dict):
    await RegistrationStates.RegistrationComplete.set()

    from_chat_id = int(callback_data.get("from_chat_id"))
    target_message_id = int(callback_data.get("message_id"))
    global GLOBAL_MODERATOR_ID
    user_id_for_moder = GLOBAL_MODERATOR_ID
    await dp.bot.send_message(from_chat_id, text="Вы ввели : " + str(user_id_for_moder))

    await callback.message.delete_reply_markup()


    all_users_ids = await get_all_user_ids()
    check_registrate = False
    for user_id in all_users_ids:
        if int(user_id) == int(user_id_for_moder):
            check_registrate = True
            break

    try:
        if check_registrate:
            existing_user = await User.get(user_id_for_moder)
            await existing_user.update(is_moderator=True).apply()
        else:

            user = User()
            user.id = user_id_for_moder
            user.first_name = "Moderator"
            user.last_name = "GASU"
            user.username = "GASUModer"
            user.group = "Administration"
            user.daily_subscription_on = False
            user.weekly_subscription_on = False
            user.is_moderator = True
            await create_user(user)
        await dp.bot.send_message(from_chat_id, text="Пользователь успешно добавлен в список модераторов.")
    except:
        pass
        await dp.bot.send_message(from_chat_id, text="Ошибка! Пользователь не создал чат с ботом!")

