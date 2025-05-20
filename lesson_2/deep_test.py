import telebot


# help_text = """
# <b>Доступные команды:</b>

# <pre>
# | Команда | Описание          |
# |---------|-------------------|
# | /pay    | 💳 Способы оплаты |
# | /old    | 📅 Время в группе |
# | /web    | 🌐 Открыть сайт   |
# </pre>

# Ссылки:
# • <a href="https://вашсайт.com">Сайт</a>
# • <a href="https://instagram.com/ваш_инстаграм">Instagram</a>
# """





bot = telebot.TeleBot("7636140010:AAHS4Ko-wd5fpspkQOQn50z-NkFdWuJpJbk")

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Привет! Я ваш бот-помощник. Введите /help для списка команд.")

@bot.message_handler(commands=["help"])
def help_command(message):
    # Создаем текст справки с поддерживаемым HTML-форматированием
    help_text = """
<b>Доступные команды и ссылки:</b>

<u>Информационные команды:</u>
• <b>Оплата</b> - Информация о способах оплаты
• <b>Возраст в группе</b> - Узнать сколько времени вы в группе

<u>Ссылки:</u>
• <a href="https://вашсайт.com">Перейти на сайт</a> - Наш официальный сайт
• <a href="https://instagram.com/ваш_инстаграм">Instagram</a> - Наш Instagram
• <a href="https://vk.com/ваша_группа">VK</a> - Наша группа ВКонтакте
• <a href="https://facebook.com/ваша_страница">Facebook</a> - Наша страница Facebook
"""
    try:
        bot.send_message(message.chat.id, help_text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        # Альтернативный вариант без HTML
        bot.send_message(message.chat.id, """
Доступные команды и ссылки:

Информационные команды:
/оплата - Информация о способах оплаты
/возраст - Узнать сколько времени вы в группе

Ссылки:
Сайт: https://вашсайт.com
Instagram: https://instagram.com/ваш_инстаграм
VK: https://vk.com/ваша_группа
Facebook: https://facebook.com/ваша_страница
""")

bot.polling(none_stop=True)