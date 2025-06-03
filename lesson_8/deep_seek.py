from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = Bot(token="7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # Создаем клавиатуру с нужными параметрами
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,  # Важно для правильного отображения
        one_time_keyboard=False  # Клавиатура останется после нажатия
    )
    
    # Исправляем опечатку в тексте кнопки ("Открыть" вместо "Открыть")
    web_app_button = KeyboardButton(
        text="Открыть веб-сайт",
        web_app=WebAppInfo(url="https://github.com/DRain777/Telegram_bot")  # Убедитесь, что URL правильный
    )
    markup.add(web_app_button)
    
    await message.answer(
        "Привет, мой друг! Нажми кнопку ниже:",
        reply_markup=markup
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)