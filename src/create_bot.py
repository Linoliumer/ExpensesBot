import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env
from pathlib import Path
import models
from modules import *
from states import *


BASE_DIR = Path(__file__).resolve().parent.parent

"""----------LOGGING----------"""

formater_logging_message = logging.Formatter("------------------------\n\nTime: %(asctime)s\nLevel: %(levelname)s\nMessage: %(message)s\n")
file_log = logging.FileHandler(f"{BASE_DIR}/logs/logs.txt")
console_log = logging.StreamHandler()
file_log.setFormatter(formater_logging_message)
console_log.setFormatter(formater_logging_message)
logging.basicConfig(level=logging.INFO, handlers=(file_log, console_log))

"""----------ENV_PARS/GET_PATHS----------"""
env = Env()
env.read_env()

CONFIG_PATH = env.str('CONFIG_PATH')
CREDS_PATH = env.str('CREDS_PATH')
CLIENT_TEXT_PATH = env.str('CLIENT_TEXT_PATH')
KEYBOARD_PATH = env.str('KEYBOARD_PATH')
DATABASE_PATH = env.str('DATABASE_PATH')

"""----------PARS FILES----------"""

try:
    fConfig = File(f"{BASE_DIR}{CONFIG_PATH}")
except Exception as e:
    # Loader. Formations of elements.
    logging.error(f"Loader. Formations of elements.\nError: {str(e)}", exc_info=True)
    exit()

"""----------CONST----------"""

WEBHOOK_HOST = fConfig.text['WEBHOOK']['HOST']
WEBHOOK_PATH = f"{fConfig.text['WEBHOOK']['PATH']}{fConfig.text['TELEGRAM']['BOT_TOKEN']}"
WEBHOOK_URL = "{}{}".format(
    WEBHOOK_HOST,
    WEBHOOK_PATH
)
WEBAPP_HOST = fConfig.text['WEBAPP']['HOST']
WEBAPP_PORT = fConfig.text['WEBAPP']['PORT']

"""----------CREATING BOT----------"""

# Creating Bot object
bot = Bot(token=fConfig.text["TELEGRAM"]["BOT_TOKEN"], parse_mode=types.ParseMode.HTML)
# Creating Storage object
storage = MemoryStorage()
# Creating Dispatcher object
dp = Dispatcher(bot, storage=storage)


"""----------FORMATIONS OF ELEMENTS----------"""

try:
    # Opening a JSON file
    keyboard_file = File(f"{BASE_DIR}{KEYBOARD_PATH}")
    # Forming keyboards
    keyboard = Keyboard_App(keyboard_file)
    # Opening a JSON file
    client_text_file = File(f"{BASE_DIR}{CLIENT_TEXT_PATH}")
    # Forming client_text
    client_text = Text_App(client_text_file)
except Exception as e:
    # Loader. Formations of elements.
    logging.error(f"Loader. Formations of elements.\nError: {str(e)}", exc_info=True)
    exit()
