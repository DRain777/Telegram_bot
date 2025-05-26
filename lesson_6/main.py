import telebot
from telebot import types   # Что бы не прописывать каждый раз telebot.types 
import webbrowser
from currency_converter import CurrencyConverter

bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет введите сумму")
    bot.register_next_step_handler(message,summa)

def summa (message):
    global amount
    try:                                  #  try пытаться 
        amount = int(message.text.strip())              # strip функция для удаление лишних пробелов        #количество перевод amout    и в эту переменную буду ложить что получил от пользователя
    except ValueError:   # excep перевод кроме      
    
             bot.send_message(message.chat.id,"неверный формат введите сумму")
             bot.register_next_step_handler(message,summa)
             return # return возвращаться 
    if amount > 0:

      markup = types.InlineKeyboardMarkup(row_width=2)             # marcup перевод наценка    row-width в одном ряду 2 кнопки
      markup = types.InlineKeyboardMarkup(row_width=2)             # marcup перевод наценка    row-width в одном ряду 2 кнопки
      btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
      btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
      btn3 = types.InlineKeyboardButton("GBP/USD", callback_data="gbp/usd")
      btn4 = types.InlineKeyboardButton("ДРУГОЕ ЗНАЧЕНИЕ",callback_data="else")
    
      markup.add(btn1,btn2,btn3,btn4)
      bot.send_message(message.chat.id,"выбирите пару валют",reply_markup=markup)
    else:
        bot.send_message(message.chat.id,"Число должно быть больше 0 введите сумму")
        bot.register_next_step_handler(message,summa)  




@bot.callback_query_handler(func=lambda call: True )
def callback(call): # call вызов ()
    if call.data != "else":
        values = call.data.upper().split("/")  # upper приводит данные в верхний регистр
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id,f"Получается: {round(res, 2)}.можете заново вписать данные")
        bot.register_next_step_handler(call.message,summa)  
    else:
        bot.send_message(call.message.chat.id, "Введите пвру значений через слэш")
        bot.register_next_step_handler(call.message,my_currency)





def my_currency(message):
    try:
       values = message.text.upper().split("/") 
       res = currency.convert(amount, values[0], values[1])       
       bot.send_message(message.chat.id,f"Получается: {round(res, 2)}.можете заново вписать данные")
       bot.register_next_step_handler(message,summa)      
    except Exception:
         bot.send_message(message.chat.id,f"Что то пошло не так. Впишите значения заново ")
         bot.register_next_step_handler(message,summa)  
                  
        
 

































bot.polling(non_stop = True)
