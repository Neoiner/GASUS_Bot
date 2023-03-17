from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from loader import dp, storage
from states.registration import RegistrationStates
from states.subscription_setup import SubscriptionSetupStates
from aiogram.utils.markdown import hbold, hitalic
from keyboards.inline.subscription import cancel_subscription_setup, subscription_type_prompt, subscription_time_prompt
from keyboards.inline.subscription import daily_subscription_subtype_prompt, weekly_subscription_subtype_prompt
from keyboards.inline.subscription import subscription_preferences_check, active_subscription_prompt
from keyboards.callbackdatas.subscription_preferences_callbackdata import subscription_preferences_callback
from utils.db_api.methods.user_methods import get_user_group, set_user_subscription_status_active, \
    set_user_subscription_status_off


# handler to inform user that command are available after cancelling subscription setup
@dp.message_handler(regexp='(\/)\w+', state=[SubscriptionSetupStates.SelectType, SubscriptionSetupStates.SelectTime])
async def remind_user_he_has_to_register(message: Message):
    await message.answer(text="Чтобы пользоваться командами,\n"
                              "закончи настройку подписки или отмени её.",
                         reply_markup=cancel_subscription_setup.keyboard)


@dp.message_handler(Command("subscribe"), state=RegistrationStates.RegistrationComplete)
async def manage_subscription(message: Message):
    user_id = message.from_user.id
    user_data = await storage.get_data(user=user_id)
    subscription_data = user_data.get('subscription_preferences')

    if subscription_data is not None:
        subscription_type = subscription_data.get('type')
        subscription_subtype = subscription_data.get('subtype')
        subscription_time = subscription_data.get('time')
        subscription_group = subscription_data.get('group')

        type_text = "ежедневная" if subscription_type == "daily" else "еженедельная"

        # alias ss for shorthand if-else statement readability
        ss = subscription_subtype
        subtype_text = "на следующий день" if ss == "next" else "на текущий день" if ss == "current"\
            else "в воскресенье" if ss == "sunday" else "в понедельник"

        subscription_preferences_text = f"Параметры твоей подписки:\n\n"\
                                        f"Тип подписки - {hitalic(type_text)}\n"\
                                        f"Присылаю расписание {hitalic(subtype_text)}\n"\
                                        f"Отправляю сообщение в {hitalic(subscription_time)}\n\n"
        await message.answer(text=f"У тебя уже есть {hbold('активная подписка')}\n\n"
                                  f"{subscription_preferences_text}"
                                  f"Что ты хочешь сделать?",
                             reply_markup=active_subscription_prompt.keyboard)
    else:
        await SubscriptionSetupStates.SelectType.set()
        await message.answer(text=f"Хочешь {hitalic('подписаться')} на расписание? Круто!\n\n"
        f"Выбирай, хочешь, чтобы я присылал тебе расписание "
        f"каждый день, или 1 раз в неделю(на все дни)?\n\n"
        f"Команда вызвана случайно? Просто жми {hitalic('Отменить настройку подписки')}.",
                             reply_markup=subscription_type_prompt.keyboard)



# handler to show subscription type prompt if user sets up new subscription
@dp.callback_query_handler(text="setup_new_subscription", state=RegistrationStates.RegistrationComplete)
async def show_subscription_type_prompt(callback: CallbackQuery):
    await SubscriptionSetupStates.SelectType.set()
    await callback.message.answer(text=f"Хочешь {hitalic('подписаться')} на расписание? Круто!\n\n"
                                f"Выбирай, хочешь, чтобы я присылал тебе расписание "
                                f"каждый день, или 1 раз в неделю(на все дни)?\n\n"
                                f"Команда вызвана случайно? Просто жми {hitalic('Отменить настройку подписки')}.",
                                reply_markup=subscription_type_prompt.keyboard)


@dp.callback_query_handler(text="cancel_subscription", state=RegistrationStates.RegistrationComplete)
async def cancel_setup(callback: CallbackQuery):
    # in pm with bot, chat_id = user_id
    user_id = callback.message.chat.id
    await set_user_subscription_status_off(user_id)
    await storage.update_data(user=user_id, subscription_preferences=None)

    await callback.answer(text="Подписка успешно отменена.", show_alert=True)
    await callback.message.answer(text="Подписка отменена.")


# handler to cancel subscription setup
@dp.callback_query_handler(text="cancel_subscription_setup",
                           state=[RegistrationStates.RegistrationComplete,
                                  SubscriptionSetupStates.SelectType,
                                  SubscriptionSetupStates.SelectSubType,
                                  SubscriptionSetupStates.SelectTime])
async def cancel_setup(callback: CallbackQuery):
    await RegistrationStates.RegistrationComplete.set()
    await callback.answer(text="Настройка подписки отменена.", show_alert=True)


# handler to set up new subscription preferences
@dp.callback_query_handler(text="setup_new_subscription_preferences", state=SubscriptionSetupStates.SelectTime)
async def setup_new_subscription_preferences(callback: CallbackQuery):
    await callback.answer()
    await SubscriptionSetupStates.SelectType.set()
    await callback.message.answer(text=f"Давай настроим подписку заново.\n\n"
    f"Выбирай, хочешь, чтобы я присылал тебе расписание "
    f"каждый день, или 1 раз в неделю(на все дни)?\n\n"
    f"Отменить - просто жми {hitalic('Отменить настройку подписки')}.",
                         reply_markup=subscription_type_prompt.keyboard)


@dp.callback_query_handler(subscription_preferences_callback.filter(), state=SubscriptionSetupStates.SelectType)
async def show_subscription_subtype_prompt(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    subscription_type = callback_data.get('type')
    await SubscriptionSetupStates.SelectSubType.set()
    if(subscription_type == "daily"):
        answer_text = f"Выбрана {hitalic('ежедневная')} подписка.\n\n" \
                      f"Ты хочешь, чтобы каждый день я присылал тебе сообщение с расписанием " \
                      f"на {hbold('следующий')} день(например, в {hitalic('среду в 17:00')} я пришлю расписание на " \
                      f"{hitalic('четверг')}), или на {hbold('текущий')} день(например, в {hitalic('пятницу в 8:00')} я " \
                      f"пришлю расписание на {hitalic('пятницу')})?"
        reply_keyboard = daily_subscription_subtype_prompt.keyboard
    else:
        answer_text = f"Выбрана {hitalic('еженедельная')} подписка.\n\n" \
            f"Хочешь, чтобы я присылал тебе расписание на всю неделю {hitalic('в воскресенье')} или " \
            f"{hitalic('в понедельник')}?"
        reply_keyboard = weekly_subscription_subtype_prompt.keyboard

    await callback.message.answer(text=answer_text, reply_markup=reply_keyboard)


@dp.callback_query_handler(subscription_preferences_callback.filter(), state=SubscriptionSetupStates.SelectSubType)
async def show_subscription_time_prompt(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    await SubscriptionSetupStates.SelectTime.set()

    user_id = callback.message.chat.id
    user_group = await get_user_group(user_id=user_id)

    subscription_type = callback_data.get('type')
    subscription_subtype = callback_data.get('subtype')
    subscription_group = user_group


    answer_text = ''
    if (subscription_subtype == "next"):
        answer_text = f"Выбрано получение расписания на следующий день.\n\n"
    elif (subscription_subtype == "current"):
        answer_text = f"Выбрано получение расписания на текущий день.\n\n"
    elif (subscription_subtype == "sunday"):
        answer_text = f"Выбрано получение расписания в воскресенье.\n\n"
    else:
        answer_text = f"Выбрано получение расписания в понедельник.\n\n"

    answer_text += f"Остался последний шаг!\n" \
                   f"Выбери удобное время:"

    await callback.message.answer(text=answer_text,
                                  reply_markup=subscription_time_prompt.generate_keyboard(type=subscription_type,
                                                                                          subtype=subscription_subtype,
                                                                                          group=subscription_group))


@dp.callback_query_handler(subscription_preferences_callback.filter(set="0"), state=SubscriptionSetupStates.SelectTime)
async def show_subscription_preferences(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    subscription_type = callback_data.get('type')
    subscription_subtype = callback_data.get('subtype')
    subscription_time = callback_data.get('time')
    subscription_group = callback_data.get('group')

    if (subscription_type == "daily"):
        type_text = f"ежедневная"
    else:
        type_text = f"еженедельная"

    if (subscription_subtype == "next"):
        subtype_text = "на следующий день"
    elif (subscription_subtype == "current"):
        subtype_text = "на текущий день"
    elif (subscription_subtype == "sunday"):
        subtype_text = "в воскресенье"
    else:
        subtype_text = "в понедельник"

    answer_text = f"Параметры твоей подписки:\n\n" \
                  f"Тип подписки - {hitalic(type_text)}\n" \
                  f"Присылаю расписание {hitalic(subtype_text)}\n" \
                  f"Отправляю сообщение в {hitalic(subscription_time)}\n\n" \
                  f"Всё верно?"

    await callback.message.answer(text=answer_text,
                                  reply_markup=subscription_preferences_check.generate_keyboard(
                                                                type=subscription_type,
                                                                subtype=subscription_subtype,
                                                                time=subscription_time,
                                                                group=subscription_group))



@dp.callback_query_handler(subscription_preferences_callback.filter(set="1"), state=SubscriptionSetupStates.SelectTime)
async def setup_subscription(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer(text="Подписка успешно оформлена!")

    await RegistrationStates.RegistrationComplete.set()
    user_id = callback.message.chat.id
    subscription_type = callback_data.get('type')
    subscription_subtype = callback_data.get('subtype')
    subscription_time = callback_data.get('time')
    subscription_group = callback_data.get('group')

    subscription_preferences = {}
    subscription_preferences['type'] = subscription_type
    subscription_preferences['subtype'] = subscription_subtype
    subscription_preferences['time'] = subscription_time
    subscription_preferences['group'] = subscription_group

    await storage.update_data(user=user_id, subscription_preferences=subscription_preferences)
    await set_user_subscription_status_active(user_id=user_id, subscription_type=subscription_type)





