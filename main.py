import webbrowser

import telebot
from telebot import types

import sqlite3

bot = telebot.TeleBot('6232113770:AAFmOfAPumuyScx7kBJAYuYylIaxt0XGuZk')

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
    name = mess.text.strip() # удаление лишних пробелов справа и слева
    bot.send_message(mess.chat.id, 'Введи пароль!')
    bot.register_next_step_handler(mess, user_pass)

def user_pass(mess):
    password = mess.text.strip()

    con = sqlite3.connect('db.sql')  # создание подключения к файлу БД
    cur = con.cursor()  # создание курсора через который происходит взаимодействие с БД
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    #     IF NOT EXISTS -- если такой таблицы не существует
    #       auto_increment -- автоматически увеличивается
    #       primary key  -- первичный ключ обьекта
    con.commit()  # создание определенной таблицы в БД
    cur.close()  # закрытие курсора -- БД
    con.close()  # закрытие соединения с Бд

    # bot.send_message(mess.chat.id, 'Введи пароль!')
    # bot.register_next_step_handler(mess, user_pass)


# два способа -- прога работает постоянно
# bot.polling(non_stop = True)
bot.infinity_polling()