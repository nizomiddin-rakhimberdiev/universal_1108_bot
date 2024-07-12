from aiogram import types
from aiogram.dispatcher import FSMContext
from states.all_states import Pdf_to_docState

from loader import dp

@dp.message_handler(text="PDF to Doc", state='*')
async def pdf_to_doc(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, PDF faylini yuboring:")
    await Pdf_to_docState.file.set()

