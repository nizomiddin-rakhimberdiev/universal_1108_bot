from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from states.all_states import PinterestState

@dp.message_handler(text='Pinterest downloader', state="*")
async def ask_pinterest_url(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Iltimos, pinterest url kiriting:")
    await PinterestState.link.set()


