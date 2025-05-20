

# @bot.message_handler(content_types=["photo"])
# def get_photo(massage):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton ("Прейти на сайт",url="https://google.com"))
#     markup.add(types.InlineKeyboardButton ("Удалить фото",callback_data="delete"))
#     markup.add(types.InlineKeyboardButton ("Изменить текст",callback_data="edit"))

#     bot.reply_to(massage,"класное фото!",reply_markup=markup)






import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Перейти на сайт 😎")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Удалить фото")
    btn3 = types.KeyboardButton("Изменить текст")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)
  
    file = open("./photo.jpeg","rb")
    file_video = open("./video.mp4","rb")
    #bot.send_photo(message.chat.id,file,reply_markup=markup)
    #bot.send_audio(message.chat.id,file,reply_markup=markup) 
    #bot.send_video(message.chat.id,file_video,reply_markup=markup)
    
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text.lower() == "перейти на сайт":
        bot.send_message(message.chat.id, "Сайт открывается...")
        webbrowser.open("https://google.com")
    elif message.text.lower() == "удалить фото":
        bot.send_message(message.chat.id, "Фото будет удалено при следующей загрузке")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url="https://google.com")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)

    bot.reply_to(message, "Классное фото!", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        # Удаляем сообщение с фото (которое находится перед сообщением с кнопками)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        # Также удаляем сообщение с кнопками
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == "edit":
        # Редактируем сообщение с кнопками
        bot.edit_message_text("Измененный текст", 
                            callback.message.chat.id, 
                            callback.message.message_id)

bot.polling(none_stop=True)