import webbrowser

import telebot
from telebot import types

bot = telebot.TeleBot('6232113770:AAFmOfAPumuyScx7kBJAYuYylIaxt0XGuZk')

# content_types == photo, text, audio, video
@bot.message_handler(content_types = ['photo'])
def get_photo(mess):
    # формируем кнопки
    markup = types.InlineKeyboardMarkup() # создаем обьект инлайн кнопок
    btn1 = types.InlineKeyboardButton('на сайт', url = 'https://getbootstrap.com/') # добавили 1 кнопку
    btn2 = types.InlineKeyboardButton('удалить', callback_data = 'delete') # кнопка удаления фото
    btn3 = types.InlineKeyboardButton('изменить текст', callback_data = 'edit') # кнопка редактирования текста
    # формируем ряды
    markup.row(btn1)
    markup.row(btn2, btn3)

    bot.reply_to(mess, 'Красивое фото', reply_markup=markup)



# создаем колбэки
@bot.callback_query_handler(func=lambda callback:True)
def callback_mess(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
        # message_id == индификатор сообщения. которое послали мы в ответ на картинку
    elif callback.data == 'edit':
        bot.edit_message_text('Edit texxxt', callback.message.chat.id, callback.message.message_id)


# кнопки возле поля ввода
@bot.message_handler(commands = ['start'])
def start(mess):
    markup = types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton('Первая')
    b2 = types.KeyboardButton('Вторая')
    b3 = types.KeyboardButton('Третья')
    markup.row(b1)
    markup.row(b2, b3)
    # отправка сообщения с кнопками
    # bot.send_message(mess.chat.id, 'Hello', reply_markup = markup)
    # отправка фото
    file = open('./photo/zzz.jpg', 'rb')
    bot.send_photo(mess.chat.id, file, reply_markup = markup)
    # send_audio -- отправка аудио
    # send_video -- отправка видео


    bot.register_next_step_handler(mess, on_click)

# работает при нажатии на кнопки после /start
def on_click(mess):
    if mess.text == 'Первая' :
        bot.send_message(mess.chat.id, 'Нажата первая кнопка')
    elif mess.text == 'Вторая':
        bot.send_message(mess.chat.id, 'Нажата вторая кнопка')





# два способа -- прога работает постоянно
# bot.polling(non_stop = True)
bot.infinity_polling()