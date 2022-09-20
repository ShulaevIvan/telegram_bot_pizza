from create_bot import  bot
from  keybords import admin_kb
from aiogram import  types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from database import sqllite_db


class FSMAdmin(StatesGroup):

    photo = State()
    name = State()
    description = State()
    price = State()


async def check_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Вы администратор - можете добавлять товар', reply_markup=admin_kb.button_panel_admin)

async def reset_admin(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if (current_state is None):
            return
        await state.finish()
        await message.reply('отменено')


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')

async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи описание')

async def load_desc(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Укажи цену')

async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        good_obj = {}
        async with state.proxy() as data:
            data['price'] = int(message.text)
            good_obj['photo']  = data['photo']
            good_obj['name'] = data['name']
            good_obj['description'] = data['description']
            good_obj['price']= data['price']
        await sqllite_db.sql_add_good(good_obj)
        await state.finish()
            




def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(check_admin, commands=['admin'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['загрузить'], state=None)
    dp.register_message_handler(reset_admin, state='*', commands=['отмена', 'отменить', 'ошибка'])
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desc, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    