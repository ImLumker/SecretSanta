from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from ..keyboard import send_number
from ..dispatcher import bot
from ..models import get_userid_gives_gift_to
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    text = "*Привіт!*"