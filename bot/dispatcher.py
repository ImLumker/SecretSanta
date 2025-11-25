""" Bot settings """
import os

from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

