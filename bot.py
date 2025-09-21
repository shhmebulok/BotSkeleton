from telebot import TeleBot
from telebot.types import Message
from log_functions import log_error
from config import TOKEN

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, 'Привет')
    return 1


try:
    bot.polling(non_stop=True)
except Exception as e:
    log_error(e)
