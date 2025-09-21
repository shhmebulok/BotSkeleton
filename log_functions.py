# It's a Telegram bot (log functions)

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import os
from datetime import datetime

import config


# ---------------------------------------------------------------------------------------------------------------------


def log(text):
    log_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    log_file = open(os.path.join(config.path, 'logs', 'logs.txt'), 'a', encoding='utf-8')
    print(f'{log_time} -- {text}')
    print(f'{log_time} -- {text}', file=log_file)
    log_file.close()


def log_error(log_text):
    log_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    error_file = open(os.path.join(config.path, 'logs', 'error-logs.txt'), 'a', encoding='utf-8')
    print(f'{log_time} -- {log_text}', file=error_file)
    error_file.close()
