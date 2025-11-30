from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

delete_form_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Я не заповнював анкету/видалити анкету',
                                                                callback_data='delete_form')]])

admin_panel_buttons = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Розпочати гру'), KeyboardButton(text='Закінчити гру'),
                                                     KeyboardButton(text='Список учасників')]])

confirm_starting_game = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅',
                                                                callback_data='confirm_start')]])
confirm_finishing_game = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅',
                                                                callback_data='confirm_finish')]])