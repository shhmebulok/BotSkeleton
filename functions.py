# It's a Telegram bot (functions)
import time
from threading import Thread

from telebot.types import Message

import config


# ---------------------------------------------------------------------------------------------------------------------
# import libraries


# ---------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

# determining the user's access rights in the bot
def auth(message: Message) -> str:
    """Return the role of user in bot"""
    # admin
    if message.from_user.id in config.ADMIN_IDS:
        return 'admin'
    # customer/executor
    else:
        return 'user'


# get username of user
def get_username(message: Message) -> str:
    """Return the username of user"""
    username = ''
    if message.from_user.first_name is not None:
        username += message.from_user.first_name
    if message.from_user.last_name is not None:
        username += message.from_user.last_name

    if username == '':
        if message.from_user.username is not None:
            username += f' @{message.from_user.username}'
        else:
            username = str(message.from_user.id)
    return username


# anti sleep class
class AntiSleep(Thread):
    def __init__(self, bot_app):
        Thread.__init__(self)
        self.work = 0
        self.bot = bot_app

    def run(self):
        self.work = 1
        while self.work == 1:
            time.sleep(30)
            self.bot.get_me()
