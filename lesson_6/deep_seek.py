import telebot
from telebot import types  # Для удобной работы с кнопками
from currency_converter import CurrencyConverter  # Для конвертации валют

# Инициализация бота и конвертера валют
bot = telebot.TeleBot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
currency = CurrencyConverter()
amount = 0  # Глобальная переменная для хранения суммы конвертации

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    """Отправляет приветственное сообщение и запрашивает сумму для конвертации"""
    bot.send_message(message.chat.id, "Привет! Введите сумму для конвертации:")
    # Регистрируем следующий шаг - функция summa получит введенную сумму
    bot.register_next_step_handler(message, summa)

def summa(message):
    """Обрабатывает введенную сумму и предлагает выбрать валютную пару"""
    global amount  # Используем глобальную переменную amount
    
    try:
        # Пытаемся преобразовать введенный текст в целое число
        amount = int(message.text.strip())  # strip() удаляет лишние пробелы
    except ValueError:
        # Если преобразование не удалось (введено не число)
        bot.send_message(message.chat.id, "Неверный формат! Введите целое число:")
        # Снова запрашиваем сумму
        bot.register_next_step_handler(message, summa)
        return
    
    # Проверяем, что сумма положительная
    if amount > 0:
        # Создаем клавиатуру с кнопками выбора валютных пар
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Создаем кнопки с популярными валютными парами
        btn1 = types.InlineKeyboardButton("USD → EUR", callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton("EUR → USD", callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton("GBP → USD", callback_data="gbp/usd")
        btn4 = types.InlineKeyboardButton("Другая валюта", callback_data="else")
        
        # Добавляем кнопки в клавиатуру
        markup.add(btn1, btn2, btn3, btn4)
        
        # Отправляем сообщение с клавиатурой
        bot.send_message(message.chat.id, "Выберите пару валют:", reply_markup=markup)
    else:
        # Если сумма отрицательная или нулевая
        bot.send_message(message.chat.id, "Число должно быть больше 0. Введите сумму:")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """Обрабатывает нажатие кнопок с валютными парами"""
    if call.data != "else":
        # Если выбрана стандартная валютная пара
        try:
            # Разделяем пару валют (например, "usd/eur" -> ["USD", "EUR"])
            values = call.data.upper().split("/")
            
            # Выполняем конвертацию
            res = currency.convert(amount, values[0], values[1])
            
            # Отправляем результат с округлением до 2 знаков после запятой
            bot.send_message(
                call.message.chat.id,
                f"Результат: {amount} {values[0]} = {round(res, 2)} {values[1]}\n"
                "Можете ввести новую сумму:"
            )
            
            # Предлагаем ввести новую сумму
            bot.register_next_step_handler(call.message, summa)
        except Exception as e:
            # Обработка ошибок конвертации
            bot.send_message(
                call.message.chat.id,
                f"Ошибка конвертации: {e}. Попробуйте снова:"
            )
            bot.register_next_step_handler(call.message, summa)
    else:
        # Если выбрана опция "Другая валюта"
        bot.send_message(
            call.message.chat.id,
            "Введите пару валют для конвертации через слэш (например: USD/RUB):"
        )
        # Регистрируем следующий шаг - функция custom_currency получит валютную пару
        bot.register_next_step_handler(call.message, custom_currency)

def custom_currency(message):
    """Обрабатывает пользовательский ввод валютной пары"""
    try:
        # Получаем текст сообщения и приводим к верхнему регистру
        text = message.text.strip().upper()
        
        # Проверяем формат ввода (должен содержать слэш)
        if "/" not in text:
            raise ValueError("Используйте формат: Валюта1/Валюта2")
        
        # Разделяем валюты
        values = text.split("/")
        
        # Проверяем, что введено 2 значения
        if len(values) != 2:
            raise ValueError("Нужно ввести 2 валюты через слэш")
        
        # Выполняем конвертацию
        res = currency.convert(amount, values[0], values[1])
        
        # Отправляем результат
        bot.send_message(
            message.chat.id,
            f"Результат: {amount} {values[0]} = {round(res, 2)} {values[1]}\n"
            "Можете ввести новую сумму:"
        )
        
        # Предлагаем ввести новую сумму
        bot.register_next_step_handler(message, summa)
    except Exception as e:
        # Обработка ошибок
        bot.send_message(
            message.chat.id,
            f"Ошибка: {e}. Введите пару валют заново (например: EUR/GBP):"
        )
        bot.register_next_step_handler(message, custom_currency)

# Запускаем бота в режиме нон-стоп
bot.polling(non_stop=True)