import telebot
import yt_dlp
import os

# Your actual bot token
API_TOKEN = 'Use your token'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a YouTube video link to download it in 720p.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    video_url = message.text
    try:
        # Options for downloading video and audio
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Download video and audio at 720p or lower
            'outtmpl': '%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  # Merge video and audio into mp4
            'noplaylist': True,  # Download only single video
            'quiet': True,  # Suppress output
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            final_file = f"{video_title}.mp4"  # The output file after merging

        # Send the final video
        with open(final_file, 'rb') as video:
            bot.send_video(message.chat.id, video, caption=f"Here is your video: {video_title}")

        # Remove the final video after sending
        os.remove(final_file)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
