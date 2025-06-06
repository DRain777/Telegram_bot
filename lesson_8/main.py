from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json



bot = Bot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)




@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("Открыть веб сайт",web_app=WebAppInfo(url="https://drain777.github.io/final_work_css_html/") ))
    await message.answer("Привет мой друг",reply_markup=markup)






@dp.message_handler(content_types=["web_app_data"])
async def web_app(message:types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f' Name: {res["name"]}. Email: {res["email"]}. phone:{res["phone"]} ');





















executor.start_polling(dp)










 
 
 

#async def start(message: types.Message):
    #markup = types.InlineKeyboardMarkup()
    #markup.add(types.InlineKeyboardButton("Открыть веб сайт",web_app=WebAppInfo#(url="https://drain777.github.io/final_work_css_html/") ))
#    await message.answer("Привет мой друг",reply_markup=markup)
