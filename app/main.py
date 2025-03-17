from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import logging
import os

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ENV variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN not found! Check ENV.")
    raise ValueError("TELEGRAM_TOKEN is missing!")

# Initializing the bot and dispatcher
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()

# FastAPI application
app = FastAPI()

# Connecting aiogram routes
from telegram_bot import router
dp.include_router(router)

# Webhook for Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = types.Update(**await request.json())
        logger.info(f"Received an update: {update}")
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return {"ok": False}
    return {"ok": True}
