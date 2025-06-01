import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# Инициализация бота
bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем клавиатуру
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Создаем кнопку с веб-приложением
    web_button = KeyboardButton(
        text="Открыть web", 
        web_app=WebAppInfo(url="https://illuvium.io")
    )
    
    # Добавляем кнопку в клавиатуру
    markup.add(web_button)
    
    # Отправляем сообщение с клавиатурой
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!",
        reply_markup=markup
    )

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)