from aiogram import types
from states.all_states import YoutubeState
from aiogram.dispatcher import FSMContext



from loader import dp
import os


@dp.message_handler(text="Youtube Video Downloader", state='*')
async def youtube_downloader(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, youtube video linkini kiriting:")
    await YoutubeState.link.set()

