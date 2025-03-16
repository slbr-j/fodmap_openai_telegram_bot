from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import asyncio
import os

# Keys from the environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher()

# Creating a FastAPI
app = FastAPI()


# Webhook
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return {"ok": True}


# Connecting handlers
import telegram_bot
