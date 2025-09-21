# It's a Telegram bot (config script)

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import os
import sys

import pytz

# ---------------------------------------------------------------------------------------------------------------------
# configuration

# path
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))

# timezone
TZ = pytz.timezone('Europe/Moscow')

# bot token
TOKEN = '7571624994:AAHfRL9M6oTelDEjwV_sD0TSUMRrSYllFC0'

# admins
ADMIN_IDS = []