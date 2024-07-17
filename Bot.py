import telebot
import os
import json
import time
from shutil import rmtree
import yt_dlp

# Load bot configuration
with open('./configbot.json') as archive:
    botInfo = json.load(archive)

bot = telebot.TeleBot(botInfo["TOKEN"], parse_mode='HTML')

filePath = os.getcwd() + '/Audio/'

users = {}  # Dictionary to store user data

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''<i>Welcome to MiniTake!</i> Send me a YouTube video link and I'll send you the audio in seconds.''')

# Handler for receiving text messages
@bot.message_handler(content_types=['text'])
def receive_link(message):
    users[message.chat.id] = {}  # Create an entry for the user
    users[message.chat.id]['url'] = message.text  # Store the YouTube URL

    msg = bot.send_message(message.chat.id, '''😎 <i>Downloading the music...</i>''')

    try:
        url = users[message.chat.id]['url']
        content = os.path.join(filePath, str(message.chat.id) + '/')
        content = os.path.abspath(content)
        os.makedirs(content, exist_ok=True)  # Create the directory
        file_path = os.path.join(content, 'audio.webm')  # Using .webm for direct audio stream

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(file_path, 'rb') as audio:
            bot.send_chat_action(message.chat.id, 'upload_audio')
            bot.edit_message_text(text=f'''😎 <i>Sending the audio!</i>''',
                                  chat_id=message.chat.id,
                                  message_id=msg.message_id)
            bot.send_audio(message.chat.id, audio)
            bot.edit_message_text(text=f'''🎸 <i>The music has been sent!</i>''',
      
