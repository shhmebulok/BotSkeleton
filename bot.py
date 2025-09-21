# It's a Telegram bot (main script)
import datetime

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
from telebot import TeleBot
from telebot.types import Message

from functions import auth, get_username, AntiSleep
from log_functions import log_error, log
from config import TOKEN
from models import User

bot = TeleBot(TOKEN)


# ---------------------------------------------------------------------------------------------------------------------
# The processing of incoming messages and commands
@bot.message_handler(commands=['start'])
def start_command(message: Message):
    try:
        if message.chat.type not in ['supergroup', 'group', 'channel']:
            # if user does not exist
            if not User.get(message.chat.id):
                info: dict = {'open_date': str(datetime.datetime.now())}
                User.create(
                    id=message.from_user.id,
                    balance=5.0,
                    username=message.from_user.username,
                    info=info
                )
                bot.send_message(message.chat.id, 'Вы успешно зарегистрировались')

            user_role = auth(message)
            # user role is admin
            if user_role == 'admin':
                text = f'Привет, Админ {get_username(message)}!'
                bot.send_message(message.chat.id, text)
            # user role is user
            elif user_role == 'user':
                text = f'Вы уже зарегистрированы в системе {get_username(message)}!'
                bot.send_message(message.chat.id, text)
            # unknown user role
            else:
                bot.send_message(message.from_user.id, 'Не удалось определить Вашу роль в боте, попробуйте еще раз')

    except Exception as e:
        bot.send_message(message.from_user.id, 'Возникла ошибка')
        log_error(e)


# ---------------------------------------------------------------------------------------------------------------------
# main loop

if __name__ == "__main__":
    # anti sleep
    anti_sleep_app = AntiSleep(bot)
    anti_sleep_app.start()

    log(f'Bot is running: https://t.me/{bot.get_me().username}')
    # infinite bot launch
    while True:
        try:
            bot.polling()
        except Exception as error:
            log_error(error)
