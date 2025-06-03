from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo



bot = Bot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Открыть веб сайт",web_app=WebAppInfo(url="https://drain777.github.io/final_work_css_html/") ))
    await message.answer("Привет мой друг",reply_markup=markup)



























executor.start_polling(dp)