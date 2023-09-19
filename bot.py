import asyncio
import logging
import sys
import base64
import datetime
import pytz
import random
import subprocess
import sqlite3
import paramiko
import hashlib
from urllib.parse import urlencode
from utils import hello
from botmain import commands, inline_data, inline_handler 

from aiogram.types import UserProfilePhotos
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.utils import markdown
from aiogram.handlers import CallbackQueryHandler



# Bot token can be obtained via https://t.me/BotFather
TOKEN = ("6600281143:AAEUdX9OZ0ahNGJO31udcbxOQlm0XH2rEAQ")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
router = Router()

async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)
    dp.include_router(inline_handler.router)
    dp.include_router(commands.router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())