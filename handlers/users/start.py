from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.default_keyboards import menu

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Universal botimizga xush kelibsiz.\n\n"
                         "Siz botimizning qaysi xizmatidan foydalanmoqchisiz?", reply_markup=menu)
