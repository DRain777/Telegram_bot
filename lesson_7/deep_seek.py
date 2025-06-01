from aiogram import Bot, Dispatcher, types, executor
import os

bot = Bot(token="7636140010:AAH5wrUHv8tFjOEaffgE1Ao_B8BSn8U8ROc")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    try:
        # 1. Указываем правильный путь к файлу
        audio_path = os.path.join("lesson_7", "music", "zhenya-trofimov-samolyoty.mp3")
        
        # 2. Открываем файл в бинарном режиме
        with open(audio_path, "rb") as audio_file:
            # 3. Отправляем аудио с метаданными
            await message.answer_audio(
                audio_file,
                title="Самолёты",
                performer="Женя Трофимов",
                caption="Вот вам музыка!"
            )
    except FileNotFoundError:
        await message.answer("Аудиофайл не найден 😢 Проверьте путь: " + audio_path)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)