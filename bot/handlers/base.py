from aiogram import Router, types
from aiogram.filters import Command

from ..keyboard import send_number
from ..dispatcher import bot
from ..models import get_userid_gives_gift_to
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    text = "*Привіт!*"
    await bot.send_message(chat_id=get_userid_gives_gift_to(message.from_user.id), text=text, parse_mode="Markdown")
