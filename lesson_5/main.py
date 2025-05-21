import telebot
from telebot import types
import webbrowser
import sqlite3
import requests
import json


bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
api = "a6e50a8d427b8b10c6791701feeef1af"

@bot.message_handler(commands=["start","Погода","погода"])
def start(message):
    bot.send_message(message.chat.id,"Приветы напиши названия города")




@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric&lang=ru")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message,f"Погода: {temp}")

        image = "/lesson_5/img_waather/sunny.jpg" if temp > 5.0 else "/lesson_5/img_waather/sun.jpg"
        file= open("./" + image, "rb")
        bot.send_photo(message.chat.id, file)
    else:
          bot.reply_to(message,"Город указан не верно")






























bot.polling(non_stop=True)