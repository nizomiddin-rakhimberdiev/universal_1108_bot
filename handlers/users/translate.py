from aiogram import types
from aiogram.dispatcher import FSMContext
from states.all_states import TranslateState
from keyboards.inline.inline_keyboards import languages

from loader import dp


@dp.message_handler(text='Translate bot', state="*")
async def translate(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Qaysi tilga tarjima qilmoqchisiz?", reply_markup=languages)
    await TranslateState.lang.set()
