from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from random import randint, shuffle, random, sample

from ..fsm import CreateUser
from ..keyboard import delete_form_button, start_game_admin_button, confirm_starting_game, confirm_finishing_game
from ..dispatcher import bot, admins
from ..models import get_info_about_gives_gift_to, get_all_users, find_user, delete_user, save_users, users
from ..filters.admin_filter import admin_only

router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    if not get_all_users(True)[0]["is_game_active"]:
        text = "Рік добігає кінця — час дарувати подарунки колегам та ділитися святковим настроєм! 🎁"
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        if find_user(message.from_user.id) is None:
            await message.answer(text="Напиши своє ім'я, <u>щоб було зрозуміло хто ти є</u> :)", parse_mode="HTML")
            await state.set_state(CreateUser.name)
        else:
            await message.answer("Твоя анкета вже заповнена", reply_markup=delete_form_button)
    else:
        gives_gift_to = get_info_about_gives_gift_to(message.from_user.id)
        if gives_gift_to["username"] is not None:
            text = (f"*Гру вже розпочато!*\n\n"
                    f"Твій підопічний: *{gives_gift_to["full_name"]}*\n"
                    f"Його Telegram: *@{gives_gift_to['username']}*\n"
                    f"Його побажання: *{gives_gift_to['suggestion']}*")
            await message.answer(text=text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
        else:
            text = (f"*Гру вже розпочато!*\n\n"
                    f"Твій підопічний: *{gives_gift_to["full_name"]}*\n"
                    f"Його побажання: *{gives_gift_to['suggestion']}*")
            await message.answer(text=text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")

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
    save_users(get_all_users(True) + [
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "full_name": data["name"],
            "gives_gift_to": None,
            "receives_gift_from": None,
            "suggestion": message.text.capitalize(),
        }
    ])
    await state.clear()

@router.message(Command("admin"))
@admin_only
async def admin(message: types.Message):
    await message.answer(text="Доступ надано", reply_markup=start_game_admin_button)


@router.message(lambda message: message.text == "Розпочати гру")
@admin_only
async def start_game(message: types.Message):
    if not get_all_users(True)[0]["is_game_active"]:
        await message.answer(text=f"👥 Зареєстровано гравців: *{len(get_all_users())}*", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        if len(get_all_users()) > 1:
            await message.answer(text="*Ви впевнені, що хочете розпочати таємного санту?*", parse_mode="Markdown", reply_markup=confirm_starting_game)
        else:
            await message.answer(text="Щоб розпочати гру, гравців повинно бути більше 1!")
    else:
        await message.answer(text="Гра вже розпочалась!", reply_markup=ReplyKeyboardRemove())

@router.message(lambda message: message.text == "Закінчити гру")
@admin_only
async def finish_game(message: types.Message):
    if get_all_users(True)[0]["is_game_active"]:
        await message.answer(text=f"{get_all_users(True)}", parse_mode="Markdown",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(text="*Ви впевнені, що хочете закінчити гру?*", parse_mode="Markdown",
                             reply_markup=confirm_finishing_game)
    else:
        await message.answer(text="Гра не триває!", reply_markup=ReplyKeyboardRemove())

""" Callback (InlineKeyboardButtons) """

@router.callback_query(F.data == "delete_form")
async def delete_form_callback(callback: CallbackQuery):
    delete_user(callback.from_user.id)
    await callback.answer(text="✅ Твоя анкета видалена\nВведи /start ще раз", show_alert=True)
    await callback.message.delete()

@router.callback_query(F.data == "confirm_start")
@admin_only
async def confirm_starting_game_callback(callback: CallbackQuery):
    user_ids = [user['user_id']for user in get_all_users()]
    all_users = get_all_users(True)
    for user in all_users[1:]:
        while True:
            random_index = randint(0, len(user_ids) - 1)
            if user["user_id"] != user_ids[random_index]:
                user["gives_gift_to"] = user_ids[random_index]
                user_ids.remove(user_ids[random_index])
                break
            elif (len(user_ids) == 1) and (user["user_id"] == user_ids[random_index]):
                for reset_user in all_users[1:]:
                    reset_user['gives_gift_to'] = None
                    reset_user['receives_gift_from'] = None
                    return await confirm_starting_game_callback(callback)

    for user in all_users[1:]:
        for user_receiver in all_users[1:]:
            if user["user_id"] == user_receiver["gives_gift_to"]:
                user["receives_gift_from"] = user_receiver["user_id"]
                break

    for user in all_users[1:]:
        for gifter in all_users[1:]:
            if user["gives_gift_to"] == gifter["user_id"]:
                try:
                    if gifter["username"] is not None:
                        text = (f"*🎅 Ти став Таємним Сантою!*\n\n"
                                f"Твій підопічний: *{gifter["full_name"]}*\n"
                                f"Його Telegram: *@{gifter['username']}*\n"
                                f"Його побажання: *{gifter['suggestion']}*\n\n"
                                f"Нехай подарунок буде приємною несподіванкою! 🎁")
                        await bot.send_message(chat_id=user['user_id'], text=text, parse_mode="Markdown")
                    else:
                        text = (f"*🎅 Ти став Таємним Сантою!*\n\n"
                                f"Твій підопічний: *{gifter["full_name"]}*\n"
                                f"Його побажання: *{gifter['suggestion']}*\n\n"
                                f"Нехай подарунок буде приємною несподіванкою! 🎁")
                        await bot.send_message(chat_id=user['user_id'], text=text, parse_mode="Markdown")
                except Exception as error:
                    await bot.send_message(chat_id=admins[0], text=f"{error}\n{user['user_id']}")
                break

    all_users[0]["is_game_active"] = True
    await callback.message.delete()
    save_users(all_users)
    return await callback.answer(text="✅ Успішно", show_alert=True)


@router.callback_query(F.data == "confirm_finish")
@admin_only
async def confirm_finishing_callback(callback: CallbackQuery):
    all_users = get_all_users(True)
    all_users[0]["is_game_active"] = False
    for user in all_users[1:]:
        user['gives_gift_to'] = None
        user['receives_gift_from'] = None
        await bot.send_message(chat_id=user["user_id"], text="Гра була примусово завершена!")
    await callback.message.delete()
    save_users(all_users)
    return await callback.answer(text="✅ Успішно", show_alert=True)


