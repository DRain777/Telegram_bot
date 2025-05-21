



import telebot
from telebot import types
import webbrowser
import sqlite3


bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")


name = None

@bot.message_handler(commands=["start"])
def start(message):
    connection = sqlite3.connect("file.sql")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users ( id init auto_incriment primary key,name varchar(57),pass varchrm(57))")
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id," Привет сейчас тебя зарегистрируем ! В ведите ваше имя")
    bot.register_next_step_handler(message,user_name) 

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id,'Введите пароль')
    bot.register_next_step_handler(message,user_pass) 



def user_pass(message):
    password = message.text.strip()
    connection = sqlite3.connect("file.sql")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (name,pass) VALUES ('%s','%s')" %(name ,password))

    connection.commit()
    cursor.close()
    connection.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей',callback_data="users"))
    bot.send_message(message.chat.id," Пользователь зарегистрирован",reply_markup=markup)






@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    connection = sqlite3.connect("file.sql")
    cursor = connection.cursor()
    cursor.execute("SELECT * fROM users")

    users = cursor.fetchall()
    info = ""
    for el in users:
        info += f"Имя:  {el[1]}, Пароль: {el[2]} \n   "
    
    cursor.close()
    connection.close()
    bot.send_message(call.message.chat.id, info)





bot.polling(none_stop=True)
    