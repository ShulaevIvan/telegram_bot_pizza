from aiogram.utils import executor
from aiogram import types
from database import sqllite_db
from aiogram.utils import executor
from create_bot import dp,bot
from modules import admin, client



if __name__ == '__main__':
    
    TOKEN = '5694523026:AAH5BAm4RK2DVfrA4B8nRBbi5FELWnYPALc'

    async def start(_):
        print('test - ок')
        sqllite_db.sql_start()

    admin.register_handlers_admin(dp)
    client.register_handlers_client(dp)

    # @dp.message_handler(commands=['start'])
    # async def bot_send(message: types.Message):
    #     await sqllite_db.sql_add_user(message)
    #     await bot.send_message(message.from_user.id, 'Добрый день')

    

       
    executor.start_polling(dp, skip_updates=True, on_startup=start)
    