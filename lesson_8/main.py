from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
bot = Bot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])  #  handler обработчик async асинхронный
async def start(message: type.Message):
    markup =types.ReplyKeyboardMarkup()
    # markup Разметка .Ответить Разметка клавиатуры
    markup.add(types.keyboard_button("открыть web",web_app=WebAppInfo)(url="https://illuvium.io"))   # keyboard_button    кнопка_клавиатуры
    await message.answer("Привет!", reply_markup=markup)

















executor.start_polling(dp)