import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import init_db, add_reminder

# Твой токен от BotFather
TOKEN = "ТВОЙ_ТОКЕН_ЗДЕСЬ"

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()
logging.basicConfig(level=logging.INFO) # Твое требование по логированию

# Функция, которая отправит сообщение в нужное время
async def send_reminder(user_id, text):
    await bot.send_message(user_id, f"⏰ Напоминание: {text}")

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот запущен! Отправь: 'Напомни купить хлеб через 1 мин'")

@dp.message()
async def set_reminder(message: types.Message):
    # Упрощенная логика: ставим напоминание ровно на 1 минуту для теста
    text = message.text
    wait_time = 1 # минута
    run_at = datetime.now() + timedelta(minutes=wait_time)
    
    # Сохраняем в базу и планировщик
    await add_reminder(message.from_user.id, text, run_at)
    scheduler.add_job(send_reminder, 'date', run_date=run_at, args=[message.from_user.id, text])
    
    await message.answer(f"Ок! Напомню через {wait_time} мин: {text}")

async def main():
    await init_db()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())