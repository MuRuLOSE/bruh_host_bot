from aiogram.types import UserProfilePhotos
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.utils import markdown
from aiogram.handlers import CallbackQueryHandler
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

from utils import stickers, db
from .main import bot


router = Router()


@router.message(CommandStart())
@router.message(F.text.lower=="старт" or "привет")
async def command_start_handler(message: Message) -> None:
    cursor = db.cursor
    sqlite_connection = db.sqlite_connection
    user_profile_photo = await bot.get_user_profile_photos(user_id=message.from_user.id, offset=0, limit=1)
    sqlite_insert_query = f"""
    INSERT INTO users (user_id, username)  
    SELECT {message.from_user.id}, "NULL"
    WHERE NOT EXISTS (
        SELECT 1 FROM users WHERE user_id = {message.from_user.id}
    )
    """

    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()

    now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    
    hi = ""
    if now.hour >= 0 and now.hour >= 4 and now.hour < 5:
        hi = ["Доброй ночи"]

    elif now.hour >= 5 and now.hour < 13:
        hi = ["Доброе утро"]

    elif now.hour >= 13 and now.hour <= 17:
        hi = ["Добрый день"]

    else:
        hi = ["Добрый вечер"]

    git = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")

    await message.answer_sticker(rf'{stickers.get_stickers("hi")}' )

    if len(user_profile_photo.photos) > 0:
        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)

        await bot.download_file(file.file_path, f'avatars/avatar_{message.from_user.id}.png')

        await message.answer_photo(photo=hello.gen_banner(username=message.from_user.first_name,user_id=message.from_user.id,hi=random.choice(hi),avatar=f"avatars/avatar_{message.from_user.id}.png"),caption=f'<b>Наш хостинг стабильный, дешевый и имеет свои преймущества.</b> #{git[:7]}',reply_markup=start(message.from_user.id))

    else:
        await message.answer(f'<b>{random.choice(hi)}</b>, <i>{message.from_user.first_name}</i>\n<b>Наш хостинг стабильный, дешевый и имеет свои преймущества.</b> #{git[:7]}',reply_markup=start(message.from_user.id))


@router.message()
async def echo_handler(message: types.Message) -> None:
    pass