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

from .inline_data import start, settings, buy
from utils import stickers, db
from .main import bot 

router = Router()

@router.callback_query()
async def handler_inline(call: types.CallbackQuery):
    private_key_path = 'C:/users/nuser/downloads/PON.pem'
    data = call.data.split(":")
    
    if data[0] == "why_we":
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("why_we")}')
        await bot.send_message(data[1],"<b>Наш хост не на 🐳 Docker. Преймущество в том что модули, и библеотеки не будут слетать.\n\nАвто рестарт при выключении (через бота выключаться будет)\n\nА хоть это и не совсем преймущество... Но у вас будет 💎 VDS как платформа</b>")
    elif data[0] == "add_pay":

        
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("buy")}')
        await bot.send_message(data[1],"<b>Спасибо что вы выбрали именно наш хостинг!\n\nМы используем платежную систему, чтобы деньги зачислялись быстро, и всё происходило автоматически\</b>\n\n<i>p.s Оплата с Украины через другого человека, почему? Потому что в платежной системе большая коммисия.</i>",reply_markup=buy(call.from_user.id))

    elif data[0] == "about":
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("about")}')
        await bot.send_message(data[1],"<b>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</b>")
    elif data[0] == "settings":
        
        cursor = sqlite_connection.cursor()
        user_id = call.from_user.id
        cursor.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is not None:
            username = row[0]
            if username ==  "NULL":
                await bot.send_message(data[1],"Юзернейм не установлен, пока это всё в ручном режиме")
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
        
    else:
        await bot.send_sticker(data[1],rf'{stickers.get_stickers("404")}')
        await bot.send_message(data[1],"<b>Хмм, походу кнопку которую вы нажали не была обработана разработчиками, пожалуйста сообщите об этом @MuRuLOSE</b>")


