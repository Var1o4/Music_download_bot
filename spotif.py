from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import spotipy
import yt_dlp
import os

client_id = "78533640a1bc4194ae56316017dc123d" # Сюда вводим полученные данные из панели спотифая
secret = "d8f8b962aadc409ba80ec45044ee2ab2" # Сюда вводим полученные данные из панели спотифая

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

spotify = spotipy.Spotify(auth_manager=auth_manager)

def music(result, message, bot):
    performers = ""
    music = result['name']
    for names in result["artists"]:
        performers = performers + names["name"] + ", "
    performers = performers.rstrip(", ")
    video = search(music, performers)
    name = f"{performers} - {music}"
    print(name)
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
    download(video, ydl_opts, message, bot)


def search(music, performers):
  videosSearch = VideosSearch(f'{performers} - {music}', limit = 1)
  videoresult = videosSearch.result()["result"][0]["link"]
  return videoresult

from pytube import YouTube

# ...

def download(videoresult, output_filename, message, bot):
    try:
        ydl = yt_dlp.YoutubeDL(output_filename)
        info_dict = ydl.extract_info(videoresult, download=False)

        if 'entries' in info_dict:
            info = info_dict['entries'][0]
        else:
            info = info_dict

        if 'url' in info:
            title = info['title']
            output_file = f'temp_music_2/{title}.mp3'
            ydl.download([videoresult])
            bot.send_audio(message.chat.id, open(output_file, 'rb'))
            os.remove(output_file)

        else:
            bot.send_message(message.chat.id, "Не удалось найти доступный поток для скачивания аудио.")
    except Exception as e:
         bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")




