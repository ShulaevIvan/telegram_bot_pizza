from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_btn = KeyboardButton('/загрузить')
delete_btn = KeyboardButton('/удалить')

button_panel_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(load_btn).add(delete_btn)