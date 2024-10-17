import telebot
import os
import yt_dlp

BOT_TOKEN = 'your token hear'

bot = telebot.TeleBot(BOT_TOKEN)

filePath = os.getcwd() + '/Audio/'

print('The bot is listening!')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        '''Welcome to Audio_downloder! Send me a YouTube video link, and I'll send you the audio in seconds.'''
    )

@bot.message_handler(content_types=['text'])
def receive_link(message):
    url = message.text
    msg = bot.send_message(message.chat.id, '😎 Downloading the music...')

    try:
        content = os.path.join(filePath, str(message.chat.id) + '/')
        os.makedirs(content, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': content + '%(title)s.mp3',  # Save file with video title and extension
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # Get video info
            title = info.get('title', 'audio')  # Use title or default to 'audio'
            file_path = os.path.join(content, f"{title}.mp3")  # Path to save audio

            ydl.download([url])

        with open(file_path, 'rb') as audio:
            bot.send_chat_action(message.chat.id, 'upload_audio')
            bot.edit_message_text(text='😎 Sending the audio!', chat_id=message.chat.id, message_id=msg.message_id)
            bot.send_audio(message.chat.id, audio, title=title)

        bot.edit_message_text(text='🎸 The music has been sent!', chat_id=message.chat.id, message_id=msg.message_id)

        os.remove(file_path)

        if not os.listdir(content):
            os.rmdir(content)

    except Exception as e:
        if os.path.exists(content):
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.isdir(content):
                os.rmdir(content)

        bot.edit_message_text(
            text=f'😓 Connection error! Cannot download the music.\nError: {e}',
            chat_id=message.chat.id,
            message_id=msg.message_id
        )

bot.infinity_polling()
