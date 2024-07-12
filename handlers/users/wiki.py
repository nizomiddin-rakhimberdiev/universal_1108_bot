from aiogram import types
from utils.apis.all_api import get_wikipedia_summary
from states.all_states import WikiState
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(text='Wikipedia bot', state="*")
async def wikipediaa(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, mavzuni kiriting:")
    await WikiState.text.set()
