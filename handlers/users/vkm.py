from aiogram import types
from aiogram.dispatcher import FSMContext
import yt_dlp
from states.all_states import vkm_bot

from loader import dp


@dp.message_handler(text="VKM bot", state="*")
async def vkm(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, musiqa nomini kiriting:")
    await vkm_bot.text.set()
