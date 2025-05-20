import telebot
from telebot import types
from datetime import datetime

# Инициализация бота с уникальным токеном, полученным от @BotFather
bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

# Конфигурационные константы
CHANNEL_ID = "@ваш_канал"  # Укажите username или ID вашего канала (например "@my_channel")
ADMIN_ID = 123456789  # Ваш Telegram ID для получения уведомлений (можно узнать у @userinfobot)

# Временное хранилище данных (в реальном проекте следует использовать базу данных)
user_data = {}  # Хранит информацию о пользователях: {user_id: {"joined_date": datetime}}
payments = {}   # Хранит информацию о платежах: {user_id: payment_data}

# Обработчик команды /start - главное меню бота
@bot.message_handler(commands=["start"])
def main(message):
    """
    Обрабатывает команду /start - точку входа для пользователей
    Создает запись о пользователе и показывает главное меню с кнопками
    """
    user_id = message.from_user.id
    
    # Сохраняем дату первого взаимодействия с ботом
    user_data[user_id] = {"joined_date": datetime.now()}
    
    # Создаем клавиатуру с основными кнопками
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💳 Оплата", callback_data="pay"),
        types.InlineKeyboardButton("📅 Время в группе", callback_data="old"),
        types.InlineKeyboardButton("🌐 Сайт", url="https://coinmarcetcap.com"),
    )
    
    # Отправляем приветственное сообщение с кнопками
    bot.send_message(
        message.chat.id, 
        "Привет! Я ваш бот-помощник. Выберите действие:", 
        reply_markup=markup
    )

def handle_payment_options(call):
    """
    Обрабатывает нажатие кнопки "Оплата"
    Показывает меню с выбором способа оплаты
    """
    # Создаем клавиатуру с вариантами оплаты
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💰 Криптовалюта (USDT)", callback_data="pay_crypto"),
        types.InlineKeyboardButton("💳 Банковская карта", callback_data="pay_card"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"),
    )
    
    # Редактируем текущее сообщение, заменяя его меню оплаты
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите способ оплаты:",
        reply_markup=markup
    )

def handle_group_time(call):
    """
    Обрабатывает нажатие кнопки "Время в группе"
    Показывает сколько дней пользователь взаимодействует с ботом
    """
    user_id = call.from_user.id
    
    # Проверяем, есть ли пользователь в нашей системе
    if user_id in user_data:
        # Вычисляем количество дней с момента первого взаимодействия
        days_in_group = (datetime.now() - user_data[user_id]["joined_date"]).days
        
        # Показываем всплывающее уведомление с результатом
        bot.answer_callback_query(
            call.id,
            f"Вы в группе уже {days_in_group} дней!",
            show_alert=True
        )
    else:
        # Если пользователь не найден (маловероятно, но возможно)
        bot.answer_callback_query(
            call.id,
            "Вы не в группе. Вступите, чтобы отслеживать время!",
            show_alert=True
        )

def check_subscription(user_id):
    """
    Проверяет, подписан ли пользователь на указанный канал
    Возвращает True если подписан, False если нет
    """
    try:
        # Получаем информацию о статусе пользователя в канале
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        # Проверяем, что статус соответствует подписчику/администратору/создателю
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        # В случае ошибки (например, бот не админ в канале) возвращаем False
        print(f"Ошибка проверки подписки: {e}")
        return False

def process_payment(user_id, payment_method):
    """
    Обрабатывает успешную оплату:
    1. Сохраняет информацию о платеже
    2. Проверяет подписку на канал
    3. Отправляет соответствующие сообщения
    4. Уведомляет администратора
    """
    # Записываем информацию о платеже
    payments[user_id] = {
        "method": payment_method,
        "timestamp": datetime.now(),
        "completed": True
    }
    
    # Проверяем подписку на канал
    if check_subscription(user_id):
        # Если уже подписан - просто подтверждаем оплату
        bot.send_message(
            user_id,
            "✅ Оплата прошла успешно! Вы уже подписаны на наш канал."
        )
    else:
        # Если не подписан - предлагаем подписаться
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        
        bot.send_message(
            user_id,
            f"✅ Оплата прошла успешно! Подпишитесь на наш канал {CHANNEL_ID} для получения контента:",
            reply_markup=markup
        )
    
    # Отправляем уведомление администратору
    bot.send_message(
        ADMIN_ID,
        f"💰 Новая оплата от пользователя {user_id}\n"
        f"Метод: {payment_method}\n"
        f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# Главный обработчик нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Центральный обработчик всех callback-запросов от inline-кнопок
    Перенаправляет вызовы соответствующим функциям
    """
    user_id = call.from_user.id
    
    # Определяем какая кнопка была нажата и вызываем соответствующий обработчик
    if call.data == "pay":
        handle_payment_options(call)
    elif call.data == "old":
        handle_group_time(call)
    elif call.data == "pay_crypto":
        # Обработка оплаты криптовалютой
        process_payment(user_id, "Криптовалюта (USDT)")
        bot.answer_callback_query(call.id, "Реквизиты для оплаты USDT: TABC123...")
    elif call.data == "pay_card":
        # Обработка оплаты картой
        process_payment(user_id, "Банковская карта")
        bot.answer_callback_query(call.id, "Реквизиты карты: 1234 5678 9012 3456")
    elif call.data == "back_to_main":
        # Возврат в главное меню
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main(call.message)

# Обработчик команды /check - проверка подписки на канал
@bot.message_handler(commands=["check"])
def check_subscription_cmd(message):
    """
    Обрабатывает команду /check - проверяет подписку пользователя на канал
    """
    if check_subscription(message.from_user.id):
        # Если подписан
        bot.reply_to(message, "✅ Вы подписаны на наш канал!")
    else:
        # Если не подписан - предлагаем подписаться
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        bot.reply_to(
            message,
            "❌ Вы не подписаны на наш канал. Пожалуйста, подпишитесь:",
            reply_markup=markup
        )

# Запускаем бота в режиме непрерывного опроса серверов Telegram
bot.polling(none_stop=True)