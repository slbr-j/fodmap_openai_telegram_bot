from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
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
def create_bot_and_dispatcher():
    bot = Bot(
        token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    return bot, dp


bot, dp = create_bot_and_dispatcher()

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
