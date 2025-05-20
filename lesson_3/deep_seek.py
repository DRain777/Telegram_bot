import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Перейти на сайт")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Удалить фото")
    btn3 = types.KeyboardButton("Изменить текст")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text.lower() == "перейти на сайт":
        bot.send_message(message.chat.id, "Открываю сайт Google...")
        webbrowser.open("https://google.com")
    elif message.text.lower() == "удалить фото":
        bot.send_message(message.chat.id, "Отправьте фото, чтобы удалить его")
    elif message.text.lower() == "изменить текст":
        bot.send_message(message.chat.id, "Отправьте новый текст")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейти на сайт", url="https://google.com")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)

    bot.reply_to(message, "Классное фото! Что сделать с ним?", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bot.answer_callback_query(callback.id, "Фото удалено")
        except Exception as e:
            bot.answer_callback_query(callback.id, f"Ошибка: {str(e)}")
    elif callback.data == "edit":
        try:
            bot.edit_message_text("Текст изменен", 
                                callback.message.chat.id, 
                                callback.message.message_id)
            bot.answer_callback_query(callback.id, "Текст изменен")
        except Exception as e:
            bot.answer_callback_query(callback.id, f"Ошибка: {str(e)}")

bot.polling(none_stop=True)