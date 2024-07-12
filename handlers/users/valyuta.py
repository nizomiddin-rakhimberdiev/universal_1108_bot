from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboards import currencies
from states.all_states import ValyutaState

from loader import dp

@dp.message_handler(text='Valyuta bot', state="*")
async def valyuta(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Siz qaysi davlat valyutasini bilmoqchisiz?", reply_markup=currencies)
    await ValyutaState.ccy.set()

