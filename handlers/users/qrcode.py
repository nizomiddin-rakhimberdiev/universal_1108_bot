from aiogram import types
from states.all_states import QRCodeState
from aiogram.dispatcher import FSMContext

from loader import dp

@dp.message_handler(text="QR-Code Generator", state="*")
async def qr_code_generator(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, QR-Code uchun text yoki url kiriting:")
    await QRCodeState.text.set()

