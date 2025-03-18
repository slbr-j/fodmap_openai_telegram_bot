from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import logging
import os

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ENV variables ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN not found! Check ENV.")
    raise ValueError("TELEGRAM_TOKEN is missing!")

# --- Init Bot and Dispatcher ---
bot = Bot(TELEGRAM_TOKEN, parse_mode="HTML")  # УВАГА! parse_mode глобально
dp = Dispatcher()

# --- FastAPI app ---
app = FastAPI()

# --- Routers ---
from telegram_bot import router
dp.include_router(router)

# --- Webhook endpoint ---
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = types.Update(**await request.json())
        logger.info(f"Received an update: {update}")
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.exception(f"Error in webhook: {e}")
        return {"ok": False}

    return {"ok": True}
