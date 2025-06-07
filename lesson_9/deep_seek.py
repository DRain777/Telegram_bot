from aiogram import Bot, Dispatcher, executor, types
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Покупка курса",
            description="Покупка курса: заработок на крипте",
            payload="invoice_payload",  # Уникальный идентификатор платежа
            provider_token=config.PAYMENT_TOKEN,
            currency="USD",
            prices=[types.LabeledPrice(label="Покупка курса", amount=500)],  # 5 USD (в центах)
            start_parameter="create_invoice_start_param",
            need_email=True,  # Запрос email у пользователя
            need_phone_number=True  # Запрос телефона у пользователя
        )
    except Exception as e:
        await message.answer(f"Ошибка при создании счета: {str(e)}")

@dp.pre_checkout_query_handler()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    await message.answer("Спасибо за покупку! Доступ к курсу открыт.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)