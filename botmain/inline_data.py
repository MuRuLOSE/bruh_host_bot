def start(user_id):
    b = InlineKeyboardBuilder()

    b.button(text=f"❓ Наши преймущества",callback_data=f"why_we:{user_id}")
    b.button(text=f"⁉️ Информация о нас",callback_data=f"about:{user_id}")
    b.button(text=f"🪙 Пополнить баланс",callback_data=f"add_pay:{user_id}")
    b.button(text=f"🪄 Пополнить баланс",callback_data=f"buy:{user_id}")
    b.button(text=f"⚙️ Управление вашими юзерботами",callback_data=f"settings:{user_id}")
    
    b.adjust(2,2,1)
    return b.as_markup()

def settings(username,user_id):
    b = InlineKeyboardBuilder()
    b.button(text=f"🔴 Выключить",callback_data=f"stop:{username}:{user_id}")
    b.button(text=f"🟢 Включить",callback_data=f"start:{username}:{user_id}")
    b.button(text=f"🔘 Перезагрузка",callback_data=f"restart:{username}:{user_id}")
    return b.as_markup()

def buy(user_id):
    b = InlineKeyboardBuilder()
    merchant_id = 'df489913-b39e-42d4-ae78-a27572792a0b' # ID Вашего магазина
    amount = 100 # Сумма к оплате
    currency = 'RUB' # Валюта заказа
    secret = '4f9ae210f241b7a45bf767b25fa17a53' # Секретный ключ №1 из настроек магазина
    order_id = f'{random.randint(1,8973124612874361296128736128367)}' # Идентификатор заказа в Вашей системе
    desc = user_id # Описание заказа
    lang = 'ru' # Язык формы

    sign = f':'.join([
        str(merchant_id),
        str(amount),
        str(currency),
        str(secret),
        str(order_id)
    ])

    params = {
        'merchant_id': merchant_id,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': desc,
        'lang': lang
    }
    b.button(text=f"🐙 Ссылка на оплату",callback_data=f"buy_link:{user_id}",url="https://aaio.io/merchant/pay?" + urlencode(params))
    b.button(text=f"🇺🇦 Оплата в Украине",callback_data=f"buy_ua:{user_id}",url="t.me/tot_882")
    return b.as_markup()