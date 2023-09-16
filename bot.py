import asyncio
import logging
import sys
import base64
import datetime
import pytz
import random
import subprocess

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


def get_stickers(sticker):
    stickers ={
        "hi": "CAACAgIAAxkBAAEBFIBlBYCy4MukVlSIr49yQkUcB5KqugAC8iwAAnDW4UuITBkIiCOD3zAE",
        "why_we": "CAACAgIAAxkBAAEBFJllBYwOMvkcW-jc-jqUySGkj-itrAACsDEAAuQ-2Ese8oqM19kLbDAE",
        "buy": "CAACAgIAAxkBAAEBFKdlBY52J-ZZTl27HltCV__2Koo6FQACfTEAAmAg4Uv6Bl3qFNLgGDAE",
        "about": "CAACAgIAAxkBAAEBFL5lBZIbdvns4BFn11T2Q1VOukM86gAC9zIAAjjk4UuDtDh0zf9BQDAE",
        "404": "CAACAgIAAxkBAAEBFMdlBZJiKFR3-TUqvEKpZ0N9xrTTYQACXioAAnjx2Es23p3FQ7sh_jAE"

    }
    
    return stickers.get(sticker, "Стандартный стикер не найден")

def start(user_id):
    b = InlineKeyboardBuilder()

    b.button(text=f"❓ Наши преймущества",callback_data=f"why_we:{user_id}")
    b.button(text=f"⁉️ Информация о нас",callback_data=f"about:{user_id}")
    b.button(text=f"🪙 Пополнить баланс",callback_data=f"add_pay:{user_id}")
    b.button(text=f"🪄 Пополнить баланс",callback_data=f"buy:{user_id}")
    
    b.adjust(2,2)
    return b.as_markup()

def buy(user_id):
    b = InlineKeyboardBuilder()
    b.button(text=f"🐙 Ссылка на оплату",callback_data=f"buy_link:{user_id}",url="https://some-buy.ru/")
    b.button(text=f"🇺🇦 Оплата в Украине",callback_data=f"buy_ua:{user_id}",url="t.me/tot_882")
    return b.as_markup()



@router.message(CommandStart())
@router.message(F.text.lower=="старт" or "привет")
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    now = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    
    hi = ""
    if now.hour < 5 or now.hour >= 20:
        hi = ["Доброй ночи","Спокойной ночи", "Приятных снов","Хорошего дня"]

    elif now.hour < 13:
        hi = ["Доброе утро","Добрейшего утречка","Светлого утра","Солнечного дня"]

    elif now.hour < 18:
        hi = ["Добрый день", "Хорошего дня", "Удачного дня"]

    else:
        hi = ["Добрый вечер", "Приятного вечера","Приятного отдыха"]

    git = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")

    await message.answer_sticker(rf'{get_stickers("hi")}' )
    await message.answer(f'<b>{random.choice(hi)}</b>, <i>{message.from_user.first_name}</i>\n<b>Наш хостинг стабильный, дешевый и имеет свои преймущества.</b> #{git[:7]}',reply_markup=start(message.from_user.id))

@router.callback_query()
async def handler_inline(call: types.CallbackQuery):
    
    data = call.data.split(":")
    
    if data[0] == "why_we":
        await bot.send_sticker(data[1],rf'{get_stickers("why_we")}')
        await bot.send_message(data[1],"<b>Наш хост не на 🐳 Docker. Преймущество в том что модули, и библеотеки не будут слетать.\n\nАвто рестарт при выключении (через бота выключаться будет)\n\nА хоть это и не совсем преймущество... Но у вас будет 💎 VDS как платформа</b>")
    elif data[0] == "buy":
        await bot.send_sticker(data[1],rf'{get_stickers("buy")}')
        await bot.send_message(data[1],"<b>Спасибо что вы выбрали именно наш хостинг!\n\nМы используем платежную систему, чтобы деньги зачислялись быстро, и всё происходило автоматически\</b>\n\n<i>p.s Оплата с Украины через другого человека, почему? Потому что в платежной системе большая коммисия.</i>",reply_markup=buy(call.from_user.id))
    elif data[0] == "about":
        await bot.send_sticker(data[1],rf'{get_stickers("about")}')
        await bot.send_message(data[1],"<b>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</b>")
    else:
        await bot.send_sticker(data[1],rf'{get_stickers("404")}')
        await bot.send_message(data[1],"<b>Хмм, походу кнопку которую вы нажали не была обработана разработчиками, пожалуйста сообщите об этом @MuRuLOSE</b>")
    

@router.message()
async def echo_handler(message: types.Message) -> None:
    commands = ['/start','старт','привет']
    if message.text.lower not in commands:
        await message.answer_sticker(rf'{get_stickers("404")}')
        await message.answer("<b>Нет такой команды бот в разработке, может неверно работать</b>")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())