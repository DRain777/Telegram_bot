import telebot
import webbrowser
bot = telebot.TeleBot("7636140010:AAH8KfvzSVKIJoMWqCUQ5-x-X6ukI3jw7kc")


@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}")


@bot.message_handler(commands=["site","website"])  
def site(message):
    webbrowser.open("https://coinmarketcap.com")  


@bot.message_handler(commands=["all"])
def main(message):
    bot.send_message(message.chat.id, str(message))  # выводит объект данных пользователя


@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(message.chat.id, "<b>Help</b> <em><u>information</u></em>", parse_mode="html")


@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} ")   # {message.from_user.last_name}
                 
    elif message.text.lower() == "id": 
        bot.reply_to(message,f'Id:{message.from_user.id}')   
       



bot.polling(none_stop=True)