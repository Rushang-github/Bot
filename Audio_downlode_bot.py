import telebot
import os
import time
import yt_dlp

# Hardcode your bot token here
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace with your actual bot token

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

filePath = os.getcwd() + '/Audio/'

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''<i>Welcome to MiniTake!</i> Send me a YouTube video link and I'll send you the audio in seconds.''')

# Handler for receiving text messages
@bot.message_handler(content_types=['text'])
def receive_link(message):
    url = message.text  # Get the YouTube URL directly from the message
    msg = bot.send_message(message.chat.id, '''😎 <i>Downloading the music...</i>''')

    try:
        content = os.path.join(filePath, str(message.chat.id) + '/')
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
                                  chat_id=message.chat.id,
                                  message_id=msg.message_id)

        # Remove the audio file after sending
        os.remove(file_path)

        # Remove the directory if it's empty
        if not os.listdir(content):
            os.rmdir(content)

    except Exception as e:
        if os.path.exists(content):
            # Remove the audio file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
            # Remove the directory if it exists
            if os.path.isdir(content):
                os.rmdir(content)

        bot.edit_message_text(text=f'''😓 <i>Connection error! Cannot download the music.</i>\nError: {e}''',
                              chat_id=message.chat.id,
                              message_id=msg.message_id)

if __name__ == '__main__':
    print('The bot is listening!')
    bot.infinity_polling()
