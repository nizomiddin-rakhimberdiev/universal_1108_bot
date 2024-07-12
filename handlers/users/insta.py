from aiogram import types
from states.all_states import InstaState
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(text="Instagram Video Downloader", state="*")
async def instagram_downloader(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, instagram video linkini kiriting:")
    await InstaState.link.set()
