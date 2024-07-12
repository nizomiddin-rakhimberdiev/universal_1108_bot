from aiogram import types
from utils.apis.all_api import get_weather
from aiogram.dispatcher import FSMContext
from states.all_states import WeatherState

from loader import dp

@dp.message_handler(text='Weather bot', state="*")
async def weatherr(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Iltimos, shahar nomini kiriting:")
    await WeatherState.city.set()




