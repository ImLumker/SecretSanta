""" Bot settings """
import os

from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN

ADMINS_PATH = os.path.join(os.path.dirname(__file__), '..', 'admins.txt')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

with open(ADMINS_PATH, 'r') as admins:
    admins = admins.readlines()
    admins = [int(admins[i]) for i in range(len(admins))]