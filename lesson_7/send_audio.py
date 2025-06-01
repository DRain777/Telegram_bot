from aiogram import Bot, Dispatcher, types, executor
import os

bot = Bot(token="7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    try:
        # Указываем правильный путь к аудиофайлу
        audio_path = os.path.join("lesson_7", "music", "AUD.mp3")
        
        if os.path.exists(audio_path):
            with open(audio_path, "rb") as audio:
                await message.answer_audio(
                    audio,
                    title="Аудио для вас",
                    performer="Исполнитель"
                )
        else:
            await message.answer("Аудиофайл не найден 😢")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)