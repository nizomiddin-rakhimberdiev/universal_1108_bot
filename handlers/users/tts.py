from aiogram import types
from states.all_states import text_to_speach
from aiogram.dispatcher import FSMContext

from loader import dp

@dp.message_handler(text="Text to speach bot", state="*")
async def ttsp(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, matnningizni kiriting:")
    await text_to_speach.text.set()

