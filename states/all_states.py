from aiogram.dispatcher.filters.state import StatesGroup, State

class WeatherState(StatesGroup):
    city = State()

class ValyutaState(StatesGroup):
    ccy = State()

class WikiState(StatesGroup):
    text = State()

class TranslateState(StatesGroup):
    lang = State()
    text = State()

class YoutubeState(StatesGroup):
    link = State()

class InstaState(StatesGroup):
    link = State()

class QRCodeState(StatesGroup):
    text = State()

class PinterestState(StatesGroup):
    link = State()

class Doc_to_pdfState(StatesGroup):
    file = State()

class Pdf_to_docState(StatesGroup):
    file = State()

class ChatGPTState(StatesGroup):
    text = State()

class RemoveBgState(StatesGroup):
    image = State()

class text_to_speach(StatesGroup):
    text = State()

class vkm_bot(StatesGroup):
    text = State()
    select = State()