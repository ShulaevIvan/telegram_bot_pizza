from create_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import Contact
from database import sqllite_db
from keybords.client_kb import keyboard_client


async def commands_start(message: types.Message):
    await sqllite_db.sql_add_user(message)
    await bot.send_message(message.from_user.id, f'Здравствуйте {message.from_user.full_name}!', reply_markup=keyboard_client)

async def get_menu(message: types.Message):
    await sqllite_db.sql_get_menu(message)

async def to_cart(callback: types.CallbackQuery):
    product_data = callback.message.caption.split('\n')
    user_id = callback.from_user.id
    await sqllite_db.sql_add_to_cart(user_id, product_data[0])
    await callback.answer(text='добавлено в корзину', show_alert=True)

async def cart(callback: types.Message):
    user_id = callback.from_user.id
    await sqllite_db.sql_get_cart(user_id)
    await callback.answer(text='корзина')

async def clear_cart(callback: types.Message):
    user_id = callback.from_user.id
    await sqllite_db.sql_clear_cart(user_id)
    await callback.answer(text='корзина очищена', show_alert=True)

async def pay_offline(callback: types.Message):
    await callback.answer(text='заявка отправлена', show_alert=True)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(get_menu, commands=['меню'])
    dp.register_callback_query_handler(to_cart, text='в корзину')
    dp.register_callback_query_handler(cart, text='корзина')
    dp.register_callback_query_handler(clear_cart, text='очистить корзину')
    dp.register_callback_query_handler(pay_offline, text='offline')