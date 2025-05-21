import telebot
from telebot import types
import webbrowser
import sqlite3
import requests
import json


bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
api = "a6e50a8d427b8b10c6791701feeef1af"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши название города")

@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    try:
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric&lang=ru")
        data = json.loads(res.text)
        
        if data["cod"] != 200:
            bot.reply_to(message, "Город не найден. Попробуйте ещё раз.")
            return
            
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"]
        
        bot.reply_to(message, 
                     f"Погода в {city.capitalize()}:\n"
                     f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                     f"Влажность: {humidity}%\n"
                     f"Ветер: {wind} м/с\n"
                     f"Описание: {description}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.polling(non_stop=True)