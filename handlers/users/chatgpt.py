# from aiogram import types
# from aiogram.dispatcher import FSMContext
# import openai
# from data.config import OPENAI_API_KEY

# from loader import dp, logging
# from states.all_states import ChatGPTState


# openai.api_key = OPENAI_API_KEY

# @dp.message_handler(text="Chat GPT Bot", state="*")
# async def chat_gpt(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Iltimos, so'rov kiriting:")
#     await ChatGPTState.text.set()

