from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

send_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📲 Поширити номер телефону', request_contact=True)],
])