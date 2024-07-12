from aiogram import types
from states.all_states import Doc_to_pdfState
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(text="Doc to PDF", state="*")
async def doc_to_pdf(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, doc faylni yuboring:")
    await Doc_to_pdfState.file.set()
