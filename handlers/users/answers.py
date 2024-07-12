import googletrans
from aiogram import types
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup
# from googletrans import Translator
# import openai
import qrcode
import requests
from data.config import REMOVE_BG
from PIL import Image
from io import BytesIO
import os
from docx2pdf import convert as docx_to_pdf
import instaloader
from pdf2docx import Converter
from utils.apis.all_api import get_weather, response
# from pytube import YouTube
from wikipedia import wikipedia
from gtts import gTTS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
from yt_dlp import YoutubeDL

# openai.api_key = OPENAI_API_KEY


from loader import dp, bot, logging
from states.all_states import Doc_to_pdfState, InstaState, Pdf_to_docState, PinterestState, QRCodeState, RemoveBgState, \
    ChatGPTState, TranslateState, ValyutaState, WeatherState, WikiState, YoutubeState, text_to_speach, vkm_bot


# remove bg
@dp.message_handler(content_types=[types.ContentType.PHOTO], state=RemoveBgState.image)
async def handle_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    file_name = f"{file_id}.png"
    with open(file_name, 'wb') as f:
        f.write(file.read())

    try:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(file_name, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG}
        )
        if response.status_code == requests.codes.ok:
            img = Image.open(BytesIO(response.content))

            no_bg_file_name = f"{file_id}_no_bg.png"
            img.save(no_bg_file_name, format="PNG")

            compressed_file_name = f"{file_id}_compressed_no_bg.png"
            img = img.convert("RGB")
            img.save(compressed_file_name, format="JPEG", quality=85)

            await message.reply_photo(open(no_bg_file_name, 'rb'), )
            await message.reply_photo(open(compressed_file_name, 'rb'))

            os.remove(no_bg_file_name)
            os.remove(compressed_file_name)
        else:
            await message.reply(f"Fon olib tashlashda xatolik: {response.status_code} {response.text}")
    except Exception as e:
        await message.reply(f"Fon olib tashlashda xatolik: {e}")

    os.remove(file_name)


# chat gpt
# @dp.message_handler(state=ChatGPTState.text)
# async def chat_gpt_response(message: types.Message, state: FSMContext):
#     user_message = message.text.replace('Chat GPT', '').strip()
#     response = openai.completions.create(
#         engine="davinci",
#         prompt=user_message,
#         max_tokens=150
#     )
#     await message.reply(response.choices[0].text.strip())


# doc to pdf
@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=Doc_to_pdfState.file)
async def file_upload(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    file_name = document.file_name
    with open(file_name, 'wb') as f:
        f.write(file.read())
    await message.reply("Konversatsiya boshlandi...")

    try:
        pdf_file_name = file_name.replace('.docx', '.pdf')
        docx_to_pdf(file_name, pdf_file_name)
        await message.reply_document(open(pdf_file_name, 'rb'))
        os.remove(pdf_file_name)
    except Exception as e:
        await message.reply(f"Doc ni PDF ga otqizishda xatolik yuz berdi: {e}")
    os.remove(file_name)


# insta
@dp.message_handler(state=InstaState.link)
async def instagram(message: types.Message, state: FSMContext):
    url = message.text
    if "instagram.com" in url:
        try:
            loader = instaloader.Instaloader()
            logging.getLogger("instaloader").setLevel(logging.CRITICAL)
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            if post.is_video:
                video_url = post.video_url
                video_data = requests.get(video_url).content
                video_path = f"{shortcode}.mp4"
                with open(video_path, 'wb') as file:
                    file.write(video_data)
                await message.reply("Video yuklab olindi hozir yuboraman...")
                await bot.send_video(message.chat.id, open(video_path, "rb"))
                os.remove(video_path)
            else:
                await message.answer("Bu video instagramda yo'q")
        except Exception as e:
            await message.answer(f"Instagramdan video yuklashda xatolik yuz berdi: {e}")
    else:
        await message.answer("Bu link instagram emas!")


# pdf to doc
@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=Pdf_to_docState.file)
async def pdf_to_docc(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    file_name = document.file_name
    with open(file_name, 'wb') as f:
        f.write(file.read())
    await message.reply("Konvertatsiya boshlandi...")

    try:
        docx_file_name = file_name.replace('.pdf', '.docx')
        cv = Converter(file_name)
        cv.convert(docx_file_name, start=0, end=None)
        cv.close()
        await message.reply_document(open(docx_file_name, 'rb'), caption="Sizning DOC faylingiz")
        os.remove(docx_file_name)
    except Exception as e:
        await message.reply(f"PDF ni Doc ga otqizishda xatolik yuz berdi: {e}")
    os.remove(file_name)


# pinterest
@dp.message_handler(state=PinterestState.link)
async def get_pinterest_url(message: types.Message, state: FSMContext):
    url = message.text
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        video_tag = soup.find('video')
        img_tag = soup.find('img')

        if video_tag:
            video_url = video_tag['src']
            video_data = requests.get(video_url).content
            video_path = "pinterest_video.mp4"
            with open(video_path, 'wb') as file:
                file.write(video_data)
            await message.reply("Kontent yuklab olindi hozir yuboraman...")
            await bot.send_video(message.chat.id, open(video_path, "rb"))
            os.remove(video_path)
        elif img_tag:
            img_url = img_tag['src']
            img_data = requests.get(img_url).content
            img_path = "pinterest_image.png"
            with open(img_path, 'wb') as file:
                file.write(img_data)
            await message.reply("Kontent yuklab olindi hozir yuboraman...")
            await bot.send_photo(message.chat.id, open(img_path, "rb"))
            os.remove(img_path)
        else:
            await message.reply("Bu kontent pinterestda yo'q")
    except Exception as e:
        await message.reply(f"Kontent yuklashda xatolik yuz berdi {e}")


# qrcode
@dp.message_handler(state=QRCodeState.text)
async def qr_codee(message: types.Message, state: FSMContext):
    url = message.text
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = "qrcode.png"
        img.save(qr_path)
        await message.reply("QR-Code yuklab olindi hozir yuboraman...")
        await bot.send_photo(message.chat.id, open(qr_path, 'rb'))
        os.remove(qr_path)
    except Exception as e:
        await message.answer(f"QR-Code yaratishda xatolik yuz berdi: {e}")


# translate
@dp.callback_query_handler(lambda query: query.data.startswith("lang_"), state=TranslateState.lang)
async def translate_text_handler(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split('_')[1]
    await state.update_data(lang=lang)
    await call.message.answer("Tarjima qilmoqchi bo'lgan matnni kirIting:")
    await TranslateState.text.set()


@dp.message_handler(state=TranslateState.text)
async def translate_text(message: types.Message, state: FSMContext):
    # translate = googletrans.Translator()
    text = message.text
    data = await state.get_data()
    lang = data['lang']
    result = googletrans.translate(text, lang)
    await message.answer(f"Tarjima qilingan matn:\n\n{result}")


# valyuta
@dp.callback_query_handler(lambda query: query.data.startswith("ccy_"), state=ValyutaState.ccy)
async def ccy(call: types.CallbackQuery):
    ccy = call.data[4:]
    for i in response:
        if i['Ccy'] == ccy:
            text = f"1 {i['CcyNm_UZ']} - {i['Rate']} so'm"
            await call.message.answer(text)


# weather
@dp.message_handler(state=WeatherState.city)
async def weather_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_info = get_weather(city)
    await message.reply(weather_info)


# youtube
async def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(result)
            return video_path
    except Exception as e:
        raise Exception(f"Video yuklashda xatolik yuz berdi: {e}")


@dp.message_handler(state=YoutubeState.link)
async def youtube(message: types.Message, state: FSMContext):
    url = message.text

    if "youtube.com" in url or "youtu.be" in url:
        try:
            await message.reply("Video yuklanb olinyapti...")
            video_path = await download_youtube_video(url)
            await message.reply("Video yuklab olindi hozir yuboraman...")
            await bot.send_video(message.chat.id, open(video_path, 'rb'))
            os.remove(video_path)
        except Exception as e:
            await message.answer(f"YouTube dan video yuklashda xatolik yuz berdi: {e}")
    else:
        await message.answer("Bu link youtube emas!")


# wiki
wikipedia.set_lang('uz')


@dp.message_handler(state=WikiState.text)
async def echoo(message: types.Message):
    text = message.text
    try:
        respond = wikipedia.summary(text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid maqola topilmadi")


# tts
@dp.message_handler(state=text_to_speach.text)
async def speach(message: types.Message, state: FSMContext):
    text = message.text
    await message.reply(f"'{text}' matni ovozli faylga aylantirilmoqda...")

    try:
        tts = gTTS(text, lang='en')
        file_path = f"tts_output.mp3"
        tts.save(file_path)

        with open(file_path, 'rb') as audio:
            await message.reply_audio(audio, title="TTS Output")

        os.remove(file_path)
    except Exception as e:
        await message.reply("Kechirasiz, ovozli fayl yaratishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        logging.error(f"Error: {e}")


# vkm bot

async def download_music(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if 'entries' in info_dict:
            video = info_dict['entries'][0]
        else:
            video = info_dict
        file_path = ydl.prepare_filename(video).rsplit('.', 1)[0] + '.mp3'
        return file_path


@dp.message_handler(state=vkm_bot.text)
async def search_music(message: types.Message):
    query = message.text
    await message.reply(f"'{query}' uchun musiqa qidiryapman...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'default_search': 'ytsearch',  # Qidiruv uchun `ytsearch` ni belgilaymiz
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(query, download=False)
            if 'entries' in info_dict:
                videos = info_dict['entries']
            else:
                videos = [info_dict]

            keyboard = InlineKeyboardMarkup()
            for idx, video in enumerate(videos[:10], start=1):  # Faqat 10 ta natijani ko'rsatish
                video_title = video['title']
                video_url = video['webpage_url']
                keyboard.add(InlineKeyboardButton(f"{idx}. {video_title}", callback_data=video_url))

            await message.reply("Mana qidiruv natijalari:", reply_markup=keyboard)
            await vkm_bot.select.set()
        except Exception as e:
            await message.reply("Kechirasiz, musiqa topilmadi. Iltimos, qayta urinib ko'ring.")
            logging.error(f"Error: {e}")


@dp.callback_query_handler(lambda c: True, state=vkm_bot.select)
async def process_callback(callback_query: types.CallbackQuery):
    url = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Musiqa yuklanmoqda...")

    try:
        file_path = await download_music(url)
        with open(file_path, 'rb') as audio:
            await bot.send_audio(callback_query.from_user.id, audio, title=os.path.basename(file_path))
        os.remove(file_path)  # Yuklab olingan faylni o'chirish
    except Exception as e:
        await bot.send_message(callback_query.from_user.id,
                               "Kechirasiz, musiqa yuklanishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        logging.error(f"Error: {e}")
