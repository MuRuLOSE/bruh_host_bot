from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import json


router = Router()


with open('nicknames.json', 'r', encoding='utf-8') as f:
    nicknames = json.load(f)


class OrderFood(StatesGroup):
    choosing_nickname = State()



@router.callback_query()
async def handler_inline(call: types.CallbackQuery, state: FSMContext):
    await call.answer(
        text="Напишите ваш никнейм:",
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_nickname)

# Этап выбора блюда #


@router.message(OrderFood.choosing_nickname, F.text.not_in(nicknames))
async def nickname_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Идёт создание вашего юзербота...",
    )
    nicknames.append(message.text.lower())
    with open('nicknames.json', 'w') as f:
        json.dump(nicknames, f,ensure_ascii=False)
    await state.clear()


@router.message(OrderFood.choosing_nickname)
async def nickname_chosen_incorecctly(message: Message):
    await message.answer(
        text="Ник уже зарегистрирован, выберите другой"
    )

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отмена выбора.")

# Этап выбора размера порции и отображение сводной информации #


