from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.user_filter import IsUser


@dp.message_handler(IsUser(), state=None)
async def bot_echo(message: types.Message):
    await message.answer(text=f"Я пониманию только специальные команды.\n"
                              f"Для справки нажми сюда - /help.")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# IsUser() filter to avoid accidental bot messages echoing
#@dp.message_handler(IsUser(), state="*", content_types=types.ContentTypes.ANY)
#async def bot_echo_all(message: types.Message, state: FSMContext):
#    state = await state.get_state()
#    await message.answer(text=f"Я пониманию только специальные команды.\n"
#                             f"Для справки нажми сюда - /help.")
