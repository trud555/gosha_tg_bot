import webbrowser

import telebot
from telebot import types

import sqlite3

bot = telebot.TeleBot('6232113770:AAFmOfAPumuyScx7kBJAYuYylIaxt0XGuZk')

name = None

@bot.message_handler(commands = ['start'])
def start(mess):
    con = sqlite3.connect('db.sql') #создание подключения к файлу БД
    cur = con.cursor() #создание курсора через который происходит взаимодействие с БД
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
#     IF NOT EXISTS -- если такой таблицы не существует
#       auto_increment -- автоматически увеличивается
#       primary key  -- первичный ключ обьекта
    con.commit() # создание определенной таблицы в БД
    cur.close() # закрытие курсора -- БД
    con.close() # закрытие соединения с Бд


    bot.send_message(mess.chat.id, 'Привет, введи свое имя!')
    bot.register_next_step_handler(mess, user_name)
#     user_name  -- функция которая вызвится после введения юзером имени

def user_name(mess):
    global name
    name = mess.text.strip() # удаление лишних пробелов справа и слева
    bot.send_message(mess.chat.id, 'Введи пароль!')
    bot.register_next_step_handler(mess, user_pass)

def user_pass(mess):
    password = mess.text.strip()

    con = sqlite3.connect('db.sql')  # создание подключения к файлу БД
    cur = con.cursor()  # создание курсора через который происходит взаимодействие с БД
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))


    con.commit()  # создание определенной таблицы в БД
    cur.close()  # закрытие курсора -- БД
    con.close()  # закрытие соединения с Бд

    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Список юзеров', callback_data = 'users')
    markup.add(b1)

    bot.send_message(mess.chat.id, 'Юзер зарегистрирован!', reply_markup = markup)
    # bot.register_next_step_handler(mess, user_pass)

# ПРОСМОТР ВСЕХ ЮЗЕРОВ
@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    con = sqlite3.connect('db.sql')
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()


    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    con.close()

    bot.send_message(call.message.chat.id, info)

# два способа -- прога работает постоянно
# bot.polling(non_stop = True)
bot.infinity_polling()