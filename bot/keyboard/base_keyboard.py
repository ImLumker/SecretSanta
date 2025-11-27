from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

delete_form_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Я не заповнював анкету/видалити анкету',
                                                                callback_data='delete_form')]])