from aiogram import Bot, Dispatcher, types ,executor



bot = Bot("7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)




@dp.message_handler(commands=["start"])  
async def start(message: types.Message):
     # await bot.send_message(message.chat.id,"Привет")
      #await message.answer("Привет")
     # file = open("/some.png","rb")
     #await message.answer_photo(file)
      await message.reply("Привет")
    
    
# Создание кнопок
@dp.message_handler()
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup()  #row_width=2
    markup.add(types.InlineKeyboardButton("site", url="https://chat.deepseek.com"))
    markup.add(types.InlineKeyboardButton("hello",callback_data="Позже"))
    await message.reply("hello",reply_markup=markup)

#  НАВЕШИВАНИЯ СОБЫТИЙ НА КНОПКИ 
@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)





@dp.message_handler(commands=["replay"])
async def replay(message:types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) # скрывает кнопки через время
    markup.add(types.KeyboardButton("site")) 
    markup.add(types.KeyboardButton("website"))
    await message.answer("Скоро",reply_markup=markup) 










#@dp.message_handler()  #  можно отслеживать любые команды  (content_types=["video"]) "photo" "text"
#async def start(message: types.Message):
#    await message.answer("Привет")











    
#@dp.message_handler(content_types=["text"])
#async def void_answer(message:types.Message):
#    await message.reply("Я сейчас очень занят отвечу вам при первой возможности")    # reply отвечать 
#    await message.answer_photo("/lesson_7/photo_telegram_bot/прикольные-отклытки-на-тему-погоды-смешные-открытки-про-погоду-разные-1135.jpg")





























#@dp.message_handler(content_types=types.ContentType.TEXT)
#async def void_answer(message: types.Message):
    # Отправляем текстовый ответ
   # await message.reply("Я сейчас очень занят, отвечу вам при первой возможности")
    
    # Отправляем фото (убедитесь, что путь правильный)
  #  try:
   #     with open("lesson_7/photo_telegram_bot/прикольные-отклытки-на-тему-погоды-смешные-открытки-про-погоду-разные-1135.jpg", "rb") as photo:
   #         await message.answer_photo(photo)
 #   except FileNotFoundError:
 #       await message.answer("Извините, фото не найдено")



executor.start_polling(dp)






