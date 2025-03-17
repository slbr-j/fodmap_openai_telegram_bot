from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import logging
import os

# Налаштовуємо логер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Keys from the environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN is missing! Check your environment variables.")

# Ініціалізація бота та диспетчера
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()

# Створюємо FastAPI
app = FastAPI()

# Підключаємо router ДО webhook
from telegram_bot import router
dp.include_router(router)


# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = types.Update(**await request.json())
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return {"ok": False}
    return {"ok": True"}
