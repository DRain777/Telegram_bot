import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

# Храним информацию о пользователях (в реальном проекте лучше использовать БД)
user_data = {}

@bot.message_handler(commands=["start"])
def main(message):
    user_id = message.from_user.id
    user_data[user_id] = {"joined_date": datetime.now()}  # Запоминаем дату вступления
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💳 Оплата", callback_data="pay"),
        types.InlineKeyboardButton("📅 Время в группе", callback_data="old"),
        types.InlineKeyboardButton("🌐 Сайт", url="https://coinmarcetcap.com"),
    )
    
    bot.send_message(
        message.chat.id, 
        "Привет! Я ваш бот-помощник. Выберите действие:", 
        reply_markup=markup
    )

# Обработчик кнопки "💳 Оплата"
def handle_payment_options(call):
    user_id = call.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("💰 Криптовалюта (USDT)", callback_data="pay_crypto"),
        types.InlineKeyboardButton("💳 Банковская карта", callback_data="pay_card"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"),
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите способ оплаты:",
        reply_markup=markup
    )

# Обработчик кнопки "📅 Время в группе"
def handle_group_time(call):
    user_id = call.from_user.id
    if user_id in user_data:
        join_date = user_data[user_id]["joined_date"]
        days_in_group = (datetime.now() - join_date).days
        bot.answer_callback_query(
            call.id,
            f"Вы в группе уже {days_in_group} дней!",
            show_alert=True
        )
    else:
        bot.answer_callback_query(
            call.id,
            "Вы не в группе. Вступите, чтобы отслеживать время!",
            show_alert=True
        )

# Главный обработчик нажатий
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pay":
        handle_payment_options(call)
    elif call.data == "old":
        handle_group_time(call)
    elif call.data == "pay_crypto":
        bot.answer_callback_query(call.id, "Реквизиты для оплаты USDT: TABC123...")
    elif call.data == "pay_card":
        bot.answer_callback_query(call.id, "Реквизиты карты: 1234 5678 9012 3456")
    elif call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        main(call.message)  # Возвращаемся в главное меню

bot.polling(none_stop=True)