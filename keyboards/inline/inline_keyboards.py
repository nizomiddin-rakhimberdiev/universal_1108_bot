from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.apis.all_api import response

currencies = InlineKeyboardMarkup(row_width=5)

currencies_btn = []
for i in response:
    currencies_btn.append(InlineKeyboardButton(text=i['Ccy'], callback_data=f"ccy_{i['Ccy']}"))

currencies.add(*currencies_btn)

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ENG", callback_data="lang_en"),
            InlineKeyboardButton(text="RUS", callback_data="lang_ru"),
            InlineKeyboardButton(text="UZB", callback_data="lang_uz"),
            InlineKeyboardButton(text="ARA", callback_data="lang_ar"),
            InlineKeyboardButton(text="KOR", callback_data="lang_ko"),

        ]
    ]
)
