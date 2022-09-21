from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import  ContentType,  Contact

work_time_btn = KeyboardButton('/время')
workplace_btn = KeyboardButton('/расположение')
menu_btn = KeyboardButton('/меню')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
order_keybord = InlineKeyboardMarkup()
pay_keybord = InlineKeyboardMarkup()

pay_online = InlineKeyboardButton(text='оплата онлайн', url="https://ya.ru/")
pay_offline = InlineKeyboardButton(text='оплата при получении', callback_data='offline')
clear_cart = InlineKeyboardButton(text='очистить корзину', callback_data='очистить корзину')

to_cart_btn = InlineKeyboardButton(text='добавить в корзину', callback_data='в корзину')
cart_btn = InlineKeyboardButton(text='коризна', callback_data='корзина')

client_tel_btn = KeyboardButton('поделиться номером ', request_contact=True)
client_home_btn = KeyboardButton('поделиться локацией ', request_location=True)

pay_keybord.row(pay_online, pay_offline, clear_cart)
order_keybord.add(to_cart_btn, cart_btn)
keyboard_client.row(work_time_btn, workplace_btn, menu_btn).add(client_home_btn, client_tel_btn)