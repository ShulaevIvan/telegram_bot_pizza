from create_bot import bot, dp
from aiogram import types, Dispatcher
from database import sqllite_db
from keybords.client_kb import keyboard_client
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from email.mime.text import MIMEText
import smtplib


class FSMClient(StatesGroup):

    request_phone_number= State()
    request_address = State()


async def send_email(data):

    SMTPSRV = 'smtp.timeweb.ru'
    PORT = 25
    LOGIN = ''
    PASSWORD = ''
    
    with smtplib.SMTP(SMTPSRV, PORT) as server:
        server.login(LOGIN, PASSWORD)
        sender = ''
        receivers = ['']
        msg = MIMEText(f"""
        Телефон для  связи:  {data['phone']}, \n
        Адрес доставки:       {data['address']}, \n
        Имя: {data['name']},\n
        Фамилия: {data['last_name']},\n
        Имя телеграм : @{data['user_name']},\n
        Время заказа:{data['order_date']},\n
        
        Позиции:\n
        {data['order']} \n
                        """)

        msg['Subject'] = 'ORDER FROM BOT'
        msg['From'] = ''
        msg['To'] = ''
    
        server.sendmail(sender, receivers, msg.as_string())

    

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



async def pay_offline(callback: types.CallbackQuery, state: FSMContext):

    order_obj = dict()
    order_obj['name'] = callback.from_user.first_name
    order_obj['last_name'] = callback.from_user.last_name
    order_obj['user_name'] = callback.from_user.full_name
    order_obj['order_date'] = callback.message.date
    order_obj['order'] = callback.message.text
    user_id = callback.from_user.id
  
    await state.update_data(data=order_obj)
    await FSMClient.request_phone_number.set()
    
    await bot.send_message(user_id,  text='введите телефон длядоставки')


async  def get_client_phone(message: types.Message, state: FSMContext):

    phone = message.text
    user_id = message.from_user.id
    order_obj = {}
    async with state.proxy() as data:
        data['phone'] =  phone
        order_obj = data
    
    await state.update_data(data=order_obj)
    await FSMClient.request_address.set()

    await bot.send_message(user_id,  text='введите адрес доставки')

async def get_client_address(message: types.Message, state: FSMContext):
    address = message.text
    user_id = message.from_user.id
    order_obj = {}

    async with state.proxy() as data:
        data['address'] =  address
        order_obj = data
        
    await state.update_data(data=order_obj)
    await send_email(order_obj)
    
    await bot.send_message(user_id,  text='вам перезвонят для уточнения заказа')
    await state.finish()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(get_menu, commands=['меню'])
    dp.register_callback_query_handler(to_cart, text='в корзину')
    dp.register_callback_query_handler(cart, text='корзина')
    dp.register_callback_query_handler(clear_cart, text='очистить корзину')
    dp.register_callback_query_handler(pay_offline, text='offline', state=None)
    dp.register_message_handler(get_client_phone, state=FSMClient.request_phone_number)
    dp.register_message_handler(get_client_address, state=FSMClient.request_address)