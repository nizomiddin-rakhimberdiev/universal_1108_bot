from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Valyuta bot"),
            KeyboardButton("Weather bot"),
        ],
        [
            KeyboardButton("Translate bot"),
            KeyboardButton("Wikipedia bot"),
        ],
        [
            KeyboardButton("Youtube Video Downloader"),
            KeyboardButton("Instagram Video Downloader")
        ],
        [
            KeyboardButton("QR-Code Generator"),
            KeyboardButton("Pinterest downloader")
        ],
        [
            # KeyboardButton("Chat GPT Bot"),
            KeyboardButton("VKM bot"),
            KeyboardButton("Remove Background")
        ],
        [
            KeyboardButton("Doc to PDF"),
            KeyboardButton("PDF to Doc")
        ],
        [
            KeyboardButton("Text to speach bot"),

        ]
    ],
    resize_keyboard=True, one_time_keyboard=True)
