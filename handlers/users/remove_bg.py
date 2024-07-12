from aiogram import types
from states.all_states import RemoveBgState
from loader import dp, bot
from aiogram.dispatcher import FSMContext


from data.config import REMOVE_BG

import requests
import os

@dp.message_handler(text='Remove Background', state="*")
async def remove_bg_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, rasm kiriting:")
    await RemoveBgState.image.set()

