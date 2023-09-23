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

from .inline_data import start, settings, buy, buy_host
from utils import stickers, db
from .main import bot 

sqlite_connection = db.sqlite_connection

router = Router()

@router.callback_query()
async def handler_inline(call: types.CallbackQuery):
    private_key_path = 'C:/users/nuser/downloads/PON.pem'
    data = call.data.split(":")
    
    if data[0] == "why_we":
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("why_we")}')
        await bot.send_message(data[1],"<b>Наш хост не на 🐳 Docker. Преймущества в том что модули, и библеотеки не будут слетать.\n\nАвто рестарт при выключении (через бота выключаться будет)\n\nА хоть это и не совсем преймущество... Но у вас будет 💎 VDS как платформа</b>")
        
    elif data[0] == "buy_host":
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("buy")}')
        await bot.send_message(data[1],"<b>🎸 Желаете купить хостинг? Тогда кнопка ниже</b>",reply_markup=buy_host(data[1]))
    
    elif data[0] == "buy_hosting":
        pass

    elif data[0] == "about":
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("about")}')
        await bot.send_message(data[1],"<b>Этот хостинг был создан @MuRuLOSE, Хостинг пока ещё молодой, Нет отзывов - Нет доверия, но я уверяю, красть никто, ничего не будет, гарантии? Нету, но просто подумайте, делать бота, подключать платёжную систему, только для того чтобы украсть 50 рублей? :)</b>")
    elif data[0] == "settings":
        
        cursor = sqlite_connection.cursor()
        user_id = call.from_user.id
        cursor.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is not None:
            username = row[0]
            if username ==  "NULL":
                await bot.send_message(data[1],"У вас не приобретён хостинг",reply_markup=buy)
                return
            else:
                await bot.send_message(data[1],"<b>Управление вашим юзерботом</b>",reply_markup=settings(username,call.from_user.id))
    
    elif data[0] == "start":
        pass # хуй
        
    elif data[0] == "stop":
        pass # переписан

    elif data[0] == "restart":
        pass #код будет переписан нахуй

        stdin, stdout, stderr = client.exec_command(f'systemctl restart {username}')
        print(stdout.read().decode())
        client.close()
        await bot.send_message(data[2],"Попытка перезагрузки")
    await call.answer()



