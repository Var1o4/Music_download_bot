from __future__ import unicode_literals
import re
import os
import webbrowser
from telebot import types
import telebot
import yt_dlp
from spotif import music, spotify, search, download, SpotifyOAuth, SpotifyClientCredentials

bot=telebot.TeleBot('6673049165:AAEQnWknMKTMQssnrJUwm3yPfGH6pSXtrPc')

import yt_dlp


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.last_name if message.from_user.last_name is not None else '' } {message.from_user.first_name}. Вставьте ссылку на на трек из spotify или видео yootube")




@bot.message_handler(func=lambda message: True)
def handle_message(message):
    link_spotify = re.findall(r'^https?://open.spotify.com/track/[\w-]+', message.text)
    link_youtube =re.findall(r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+', message.text)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'id: {message.from_user.id}')
    elif link_youtube:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'temp_music_2/%(title)s.%(ext)s',
                'verbose': True,
            }

            ydl = yt_dlp.YoutubeDL(ydl_opts)
            info_dict = ydl.extract_info(message.text, download=False)

            if 'entries' in info_dict:
                info = info_dict['entries'][0]
            else:
                info = info_dict

            if 'url' in info:
                title = info['title']
                output_file = f'temp_music_2/{title}.mp3'
                ydl.download([message.text])
                bot.send_audio(message.chat.id, open(output_file, 'rb'))
                os.remove(output_file)
            else:
                bot.send_message(message.chat.id, "Не удалось найти доступный поток для скачивания аудио.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
    elif link_spotify:
        result =spotify.track(message.text)
        music(result, message, bot)
    else:
        bot.send_message(message.chat.id, "К сожадению это не та ссылка:(")


bot.infinity_polling()