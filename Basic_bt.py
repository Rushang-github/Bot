import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = "Your Token"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot! How can I assist you today?")

bot.polling()
