from aiogram import types
from pytube import YouTube
import instaloader
from bs4 import BeautifulSoup
import qrcode
import requests


from loader import dp, bot, logging
import os


@dp.message_handler(text="Youtube Video Downloader")
async def youtube_downloader(message: types.Message):
    await message.answer("Iltimos, youtube video linkini kiriting:")

@dp.message_handler(text="Instagram Video Downloader")
async def instagram_downloader(message: types.Message):
    await message.answer("Iltimos, instagram video linkini kiriting:")

@dp.message_handler(text='Pinterest downloader')
async def ask_pinterest_url(message: types.Message):
    await message.reply("Iltimos, pinterest url kiriting:")

@dp.message_handler(text="QR-Code Generator")
async def qr_code_generator(message: types.Message):
    await message.answer("Iltimos, QR-Code uchun text yoki url kiriting:")


@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text

    if "youtube.com" in url or "youtu.be" in url:
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video_path = video.download()
            await message.reply("Video yuklab olindi hozir yuboraman...")
            await bot.send_video(message.chat.id, open(video_path, 'rb'))
            os.remove(video_path)
        except Exception as e:
            await message.answer(f"YouTube dan video yuklashda xatolik yuz berdi: {e}")
    elif "instagram.com" in url:
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
    elif "pinterest.com" in url:
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
            await message.reply(f"Ошибка при скачивании видео с Instagram: {e}")
    else:
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
    