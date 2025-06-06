from aiogram import Bot, Dispatcher, executor, types
import config


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_invoice(message.chat.id, "Покупка курса","Покупка курса заработак на крипте","invoice",config.PAYMENT_TOKEN,"USD",[types.labeled_price("Покупка курса",5*100)])





















































