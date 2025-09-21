# It's a Telegram bot (keyboards)

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import datetime
import telebot
from telebot.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import config


# ---------------------------------------------------------------------------------------------------------------------
# keyboards

# user keyboards
# ---------------------------------------------------------------------------------------------------------------------
def user_start():
    markup = ReplyKeyboardMarkup()
