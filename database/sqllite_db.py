import sqlite3 as sq
from create_bot import bot
from keyboards.client_kb import order_keybord, pay_keybord

def sql_start():
    global base, cursor

    base = sq.connect('bot.db')
    cursor = base.cursor()

    if base:
        print('DB connect - OK')

    base.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER UNIQE,
            first_name TEXT,
            last_name TEXT,
            telegram_name TEXT
        )
    """)
    base.execute("""
        CREATE TABLE IF NOT EXISTS goods(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            img Text, 
            name TEXT, 
            description TEXT, 
            price INTEGER
        )
    """)

    base.execute("""
        CREATE TABLE IF NOT EXISTS user_goods(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id ITEGER,
            good_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(good_id) REFERENCES goods(id) ON DELETE CASCADE
        )
    """)
    base.commit()

async def sql_add_user(message):
    check_user = cursor.execute(f"""SELECT user_id FROM users  WHERE  user_id ={message.from_user.id}""").fetchall()
    if len(check_user) == 0:
        data = ((int(message.from_user.id)),message.from_user.first_name, message.from_user.last_name,message.from_user.username)
        cursor.execute('INSERT INTO users(user_id,first_name,last_name,telegram_name) VALUES(?,?,?,?)', data)
        base.commit()

async def sql_add_good(data):
    check_good = cursor.execute(f"""SELECT name FROM goods WHERE name LIKE '%{data['name']}%'""").fetchall()
    if len(check_good) == 0:
        to_db = (data['photo'],data['name'],data['description'],data['price'])
        cursor.execute('INSERT INTO goods(img,name,description,price) VALUES(?,?,?,?)', to_db)
        base.commit()

async def sql_get_menu(message):
    menu_data = cursor.execute('SELECT * FROM goods').fetchall()
    for item in menu_data:
        await bot.send_photo(message.from_user.id, item[1], f'{item[2]}\n Описание: {item[3]}\n Цена: {item[-1]} рублей',reply_markup=order_keybord)

async def sql_add_to_cart(user_id, product_name):
    product_data = cursor.execute(f'SELECT * FROM goods WHERE name LIKE "%{product_name}%"').fetchall()
    check_product_cart = cursor.execute(f'SELECT * FROM user_goods WHERE user_id={user_id} AND good_id={product_data[0][0]}').fetchall()
    if len(check_product_cart) == 0:
        to_db = (user_id, product_data[0][0], 1)
        cursor.execute('INSERT INTO user_goods(user_id, good_id, quantity) VALUES(?,?,?)', to_db)
        base.commit()
    else:
        cursor.execute(f'UPDATE user_goods SET quantity = quantity+1 WHERE user_id={user_id} AND good_id = {product_data[0][0]}; ')
        base.commit()

async def sql_get_cart(user_id):

    total_sum = 0
    result_str = []
    user_goods = cursor.execute(f'SELECT * FROM user_goods WHERE user_id = {user_id}').fetchall()

    for user_good in user_goods:
        if user_good[3] == 0:
            continue
        good_param  = cursor.execute(f'SELECT * FROM goods WHERE id= {user_good[2]}').fetchall()
        total_sum = total_sum + (int(user_good[3]) * int(good_param[0][4]))
        result_str.append(f'Наиенование: {good_param[0][2]}\n Количество: {str(user_good[3])} \n Цена за ед: {good_param[0][4]} рублей \n\n')

    if not total_sum == 0:
        await bot.send_message(str(user_id), ''.join(result_str)+f'\n Всего к оплате {total_sum} рублей', reply_markup=pay_keybord)
    else:
        await bot.send_message(str(user_id), f'Ваша корзина пуста')

    
async def sql_clear_cart(user_id):
    cursor.execute(f'UPDATE user_goods SET quantity = 0 WHERE user_id={user_id}')
    base.commit()

async def sql_get_all():
    return cursor.execute('SELECT * FROM goods').fetchall()
        
