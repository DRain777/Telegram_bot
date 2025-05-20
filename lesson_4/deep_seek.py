# Импорт необходимых библиотек
import telebot  # для работы с Telegram API
from telebot import types  # для создания кнопок и других элементов интерфейса
import sqlite3  # для работы с базой данных SQLite

# Создание экземпляра бота с вашим токеном
bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

# Глобальная переменная для хранения имени пользователя между шагами регистрации
name = None

# Обработчик команды /start - запускает процесс регистрации
@bot.message_handler(commands=["start"])
def start(message):
    """
    Начало работы с ботом. Создает таблицу users в базе данных, если она не существует,
    и запрашивает имя пользователя для регистрации.
    """
    try:
        # Подключение к базе данных (файл file.sql будет создан автоматически)
        connection = sqlite3.connect("file.sql")
        cursor = connection.cursor()
        
        # Создание таблицы users с тремя столбцами:
        # id - целое число, первичный ключ с автоинкрементом
        # name - строка длиной до 50 символов
        # pass - строка длиной до 50 символов (в реальном проекте не храните пароли в открытом виде!)
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name VARCHAR(50),
                          pass VARCHAR(50))""")
        
        connection.commit()  # Сохранение изменений в базе данных
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        # Закрытие соединения с базой данных в любом случае
        cursor.close()
        connection.close()
    
    # Запрос имени пользователя и переход к следующему шагу
    bot.send_message(message.chat.id, "Привет! Сейчас тебя зарегистрируем! Введите ваше имя")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    """
    Получает имя пользователя и запрашивает пароль.
    """
    global name
    name = message.text.strip()  # Удаляем лишние пробелы и сохраняем имя
    
    # Проверка, что имя не пустое
    if not name:
        bot.send_message(message.chat.id, "Имя не может быть пустым. Пожалуйста, введите имя еще раз.")
        bot.register_next_step_handler(message, user_name)
        return
    
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    """
    Получает пароль пользователя и сохраняет данные в базу данных.
    """
    password = message.text.strip()  # Удаляем лишние пробелы
    
    # Проверка, что пароль не пустой
    if not password:
        bot.send_message(message.chat.id, "Пароль не может быть пустым. Пожалуйста, введите пароль еще раз.")
        bot.register_next_step_handler(message, user_pass)
        return
    
    try:
        connection = sqlite3.connect("file.sql")
        cursor = connection.cursor()

        # Безопасное добавление данных с использованием параметров (защита от SQL-инъекций)
        cursor.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))

        connection.commit()  # Сохранение изменений
        
        # Создание кнопки для просмотра списка пользователей
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Список пользователей', callback_data="users"))
        
        bot.send_message(message.chat.id, "Пользователь зарегистрирован!", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при регистрации: {e}")
    finally:
        cursor.close()
        connection.close()

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Обработчик нажатия на кнопку "Список пользователей".
    Получает всех пользователей из базы данных и выводит их.
    """
    try:
        connection = sqlite3.connect("file.sql")
        cursor = connection.cursor()
        
        # Получение всех записей из таблицы users
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        # Формирование сообщения со списком пользователей
        if users:
            info = "Список зарегистрированных пользователей:\n\n"
            for user in users:
                info += f"ID: {user[0]}, Имя: {user[1]}, Пароль: {user[2]}\n"
        else:
            info = "Пока нет зарегистрированных пользователей."
        
        bot.send_message(call.message.chat.id, info)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка при получении списка пользователей: {e}")
    finally:
        cursor.close()
        connection.close()

# Запуск бота в режиме постоянного опроса сервера Telegram
bot.polling(none_stop=True)