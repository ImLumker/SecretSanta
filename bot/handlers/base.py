from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..fsm import CreateUser
from ..keyboard import delete_form_button
from ..dispatcher import bot
from ..models import get_userid_gives_gift_to, get_all_users, find_user, delete_user, save_users

router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    if find_user(message.from_user.id) is None:
        text = "Рік добігає кінця — час дарувати подарунки колегам та ділитися святковим настроєм! 🎁"
        await message.answer(text)
        await message.answer(text="Напиши своє ім'я, щоб було зрозуміло хто ти є :)", parse_mode="Markdown")
        await state.set_state(CreateUser.name)
    else:
        await message.answer("Твоя анкета вже заповнена", reply_markup=delete_form_button)

@router.message(CreateUser.name)
async def create_user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await message.answer(text="Напиши своє побажання, який подарунок ти хотів би отримати? 🎁")
    await state.set_state(CreateUser.suggestion)

@router.message(CreateUser.suggestion)
async def create_user_suggestion(message: types.Message, state: FSMContext):
    await message.answer(text="<b>Твоя анкета створена ✅</b>\n"
                              "Залишилось дочекатись поки інші заповнять їх теж\n\n"
                              "<tg-spoiler>Якщо ти хочеш змінити ім'я або побажання, то напиши /start ще раз</tg-spoiler>", parse_mode="HTML")
    data = await state.get_data()
    save_users(get_all_users() + [
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "full_name": data["name"],
            "has_gifter": False,
            "gives_gift_to": None,
            "receives_gift_from": None,
            "suggestion": message.text.capitalize(),
        }
    ])
    await state.clear()


@router.callback_query(F.data == "delete_form")
async def delete_form_callback(callback: CallbackQuery):
    delete_user(callback.from_user.id)
    await callback.answer(text="✅ Твоя анкета видалена\nВведи /start ще раз", show_alert=True)
    await callback.message.delete()