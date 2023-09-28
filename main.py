from __future__ import unicode_literals
import re
import os
import webbrowser
from telebot import types
import telebot
import yt_dlp
from spotif import music, spotify, search, download, SpotifyOAuth, SpotifyClientCredentials

# Здесь вы можете вызывать импортированные функции

# Здесь вы можете вызывать импортированные функции

# Весь остальной код main.py остается без изменений

# Здесь вы можете вызывать импортированные функции


bot=telebot.TeleBot('6673049165:AAEQnWknMKTMQssnrJUwm3yPfGH6pSXtrPc')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Go to the site')
    btn2 = types.KeyboardButton('Delete photo')
    btn3 = types.KeyboardButton('Edit text')

    markup.row(btn1)
    markup.row(btn3, btn2)
    # file = open('./Haori-Yukata.jpg', 'rb')
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Go to the site':
        bot.send_message(message.chat.id, 'website is open')
    elif message.text == 'Delete photo':
        bot.send_message(message.chat.id, 'Deleted')

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.youtube.com/watch?v=-l_CYgBj4IE&list=PL0lO_mIqDDFUev1gp9yEwmwcy8SicqKbt&index=3')


@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}')

@bot.message_handler(commands=["message"])
def mess(message):
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['photo', 'audio'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton('Go to the site', url='google.com')
    btn2=types.InlineKeyboardButton('Delete photo', callback_data='delete')
    btn3=types.InlineKeyboardButton('Edit text', callback_data='edit')


    markup.row(btn1)
    markup.row(btn3, btn2)
    bot.reply_to(message, "фото огонь", reply_markup= markup)


@bot.callback_query_handler(func= lambda callback: True)
def callback_message(callback):
    if callback.data =='delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)


import yt_dlp


# ...

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


bot.infinity_polling()