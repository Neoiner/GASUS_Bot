from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
import logging

from data.config import ADMINS
from filters import IsAdmin
from loader import dp, storage

from states.notification import Notification
from states.registration import RegistrationStates
from keyboards.inline.notification import cancel_notification_prompt, send_notification_prompt, cancel_survey_prompt
from keyboards.inline.notification import survey, send_survey_prompt
from keyboards.callbackdatas.send_notification_callbackdata import send_notification_callback
from keyboards.callbackdatas.survey_callbackdata import survey_callback
from utils.db_api.methods.user_methods import get_all_user_ids


# Notifications(or ads) handlers
@dp.message_handler(IsAdmin(), Command("notify", prefixes="!/"), state="*")
async def ask_for_notification_message(message: Message):
    await Notification.SetupMessage.set()

    await message.answer(text=f'Присылай сообщение для рассылки, '
                              f'я отправлю его копию всем зарегистрированным пользователям.',
                         reply_markup=cancel_notification_prompt.keyboard)


@dp.callback_query_handler(IsAdmin(), text="cancel_notification_setup", state=Notification.SetupMessage)
async def cancel_notification_setup(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Настройка оповещения отменена.")
    await RegistrationStates.RegistrationComplete.set()


@dp.message_handler(IsAdmin(), state=Notification.SetupMessage, content_types=types.ContentType.ANY)
async def check_notification_message(message: Message):
    admin_id = message.from_user.id

    from_chat_id = admin_id
    message_id = message.message_id

    await message.answer(text="Давай проверим сообщение перед отправкой:")
    # In pm with bot, chat_id = user_id
    await message.copy_to(chat_id=admin_id,
                          reply_markup=send_notification_prompt.generate_keyboard(from_chat_id=from_chat_id,
                                                                                  target_message_id=message_id))


@dp.callback_query_handler(IsAdmin(), text="edit_notification", state=Notification.SetupMessage)
async def edit_notification(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Пришли новое сообщение для рассылки.")


@dp.callback_query_handler(IsAdmin(), send_notification_callback.filter(), state=Notification.SetupMessage)
async def send_notification(callback: CallbackQuery, callback_data: dict):
    await RegistrationStates.RegistrationComplete.set()

    from_chat_id = int(callback_data.get("from_chat_id"))
    target_message_id = int(callback_data.get("message_id"))

    await callback.message.delete_reply_markup()

    all_users_ids = await get_all_user_ids()
    count_message = 0
    count_error_message = 0
    for user_id in all_users_ids:

        # In pm with bot, chat_id = user_id
        
        try:
            await dp.bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=target_message_id)
            count_message = count_message + 1
        except Exception as err:
            logging.exception(err)
            count_error_message = count_error_message + 1
            
    itog_message = "Рассылка успешно завершена!" + "\n Успешно отправленно: " + str(count_message - count_error_message) + " сообщений.\n Завершено с ошибкой: " + str(count_error_message) + " сообщений."
    await dp.bot.send_message(chat_id=from_chat_id, text= itog_message)


# Surveys handlers
@dp.message_handler(IsAdmin(), Command("survey", prefixes="!/"), state="*")
async def set_survey_header(message: Message):
    await Notification.SetupSurveyHeader.set()

    await message.answer(text=f'Присылай заголовок опроса.',
                         reply_markup=cancel_survey_prompt.keyboard)


@dp.callback_query_handler(IsAdmin(), text="cancel_survey_setup", state=Notification.SetupSurveyHeader)
async def cancel_survey_setup(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text="Настройка опроса отменена.")
    await RegistrationStates.RegistrationComplete.set()


@dp.message_handler(IsAdmin(), state=Notification.SetupSurveyHeader)
async def set_survey_options(message: Message):
    await Notification.SetupSurveyOptions.set()

    admin_id = message.from_user.id
    survey_details = {}
    survey_header = message.text
    survey_details['survey_header'] = survey_header
    await storage.update_data(user=admin_id, survey_details=survey_details)

    await message.answer(text="Присылай мне варианты ответа через ', '.")


@dp.message_handler(IsAdmin(), state=Notification.SetupSurveyOptions)
async def check_survey(message: Message):
    survey_options = message.text.split(', ')

    admin_id = message.from_user.id
    admin_data = await storage.get_data(user=admin_id)
    survey_details = admin_data.get('survey_details')
    survey_details['survey_options'] = survey_options
    await storage.update_data(user=admin_id, survey_details=survey_details)

    await message.answer(text=f"Так будет выглядеть опрос:")

    await message.answer(text=survey_details.get('survey_header'),
                         reply_markup=survey.generate_keyboard(survey_options))

    await message.answer(text=f"Всё готово!", reply_markup=send_survey_prompt.keyboard)


@dp.callback_query_handler(IsAdmin(), text="cancel_survey",  state=Notification.SetupSurveyOptions)
async def cancel_send_survey(callback: CallbackQuery):
    await callback.answer()

    admin_id = callback.from_user.id
    await storage.update_data(user=admin_id, survey_details=None)
    await RegistrationStates.RegistrationComplete.set()
    await callback.message.answer(text="Рассылка опроса отменена.")




@dp.callback_query_handler(IsAdmin(), text="send_survey", state=Notification.SetupSurveyOptions)
async def send_survey(callback: CallbackQuery):
    await RegistrationStates.RegistrationComplete.set()

    admin_id = callback.from_user.id
    result_message_id = callback.message.message_id

    admin_data = await storage.get_data(user=admin_id)
    survey_details = admin_data.get('survey_details')
    survey_details['admin_chat_id'] = admin_id
    survey_details['result_message_id'] = result_message_id
    await storage.update_data(user=admin_id, survey_details=survey_details)


    result_message_chat = admin_id
    await dp.bot.edit_message_reply_markup(chat_id=result_message_chat, message_id=result_message_id, reply_markup=None)


    survey_header = survey_details.get('survey_header')
    survey_options = survey_details.get('survey_options')
    admin_chat_id = survey_details.get('admin_chat_id')
    result_message_id = survey_details.get('result_message_id')
    message_text = f"Результаты опроса:\n\n"
    message_text += f"{survey_header}\n\n"
    for survey_option in survey_options:
        message_text += f"{survey_option} - 0 \n"

    # number of users that chose some option will be stored by key option%option_number% (example: option3)
    for i in range(1, len(survey_options) + 1):
        key = f"option{i}"
        survey_details[key] = 0

    await storage.update_data(user=admin_id, survey_details=survey_details)

    await dp.bot.edit_message_text(text=message_text, chat_id=admin_chat_id, message_id=result_message_id)
    await dp.bot.pin_chat_message(chat_id=admin_chat_id, message_id=result_message_id)

    all_users_ids = await get_all_user_ids()
    for user_id in all_users_ids:
        await dp.bot.send_message(chat_id=user_id, text=survey_header, reply_markup=survey.generate_keyboard(
            survey_options=survey_options, admin_chat_id=admin_chat_id, message_id=result_message_id))

    await dp.bot.send_message(chat_id=admin_chat_id, text="Рассылка опроса успешно завершена!")



# handlers to process user's survey answer
@dp.callback_query_handler(survey_callback.filter(), state="*")
async def process_survey_answer(callback: CallbackQuery, callback_data: dict):
    await callback.answer()
    callback_message_chat_id = callback.message.chat.id
    callback_message_id = callback.message.message_id

    admin_chat_id = int(callback_data.get('admin_chat_id'))
    result_message_id = int(callback_data.get('message_id'))
    option_number = int(callback_data.get('option'))

    # admin_id == admin_chat_id since in pm with bor chat_id == user_id
    admin_data = await storage.get_data(user=admin_chat_id)
    survey_details = admin_data.get('survey_details')
    survey_header = survey_details.get('survey_header')
    survey_options = survey_details.get('survey_options')

    # incrementing chosen option counter
    chosen_option_key = f"option{option_number}"
    counter = survey_details.get(chosen_option_key) + 1
    survey_details[chosen_option_key] = counter
    await storage.update_data(user=admin_chat_id, survey_details=survey_details)

    result_message_text = f"Результаты опроса:\n\n"
    result_message_text += f"{survey_header}\n\n"
    counter = 1
    for survey_option in survey_options:
        key = f"option{counter}"
        number_of_votes = survey_details.get(key)
        result_message_text += f"{survey_option} - {number_of_votes} \n"
        counter += 1

    await dp.bot.edit_message_text(text=result_message_text, chat_id=admin_chat_id, message_id=result_message_id)

    await dp.bot.edit_message_reply_markup(chat_id=callback_message_chat_id, message_id=callback_message_id,
                                           reply_markup=None)

    await dp.bot.edit_message_text(chat_id=callback_message_chat_id, message_id=callback_message_id,
                                   text="Спасибо за участие в опросе!")




