from aiogram import types, Router
from aiogram.filters import Command
from assistants_api import ask_assistant
from keyboards import get_main_keyboard
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"User {message.from_user.id} started a session.")
    await message.answer(
        "Hi! I'm a FODMAP assistant 👩🏻‍⚕️\n\nHow can I help?",
        reply_markup=get_main_keyboard()
    )

@router.message()
async def handle_text(message: types.Message):
    user_input = message.text
    logger.info(f"Question from {message.from_user.id}: {user_input}")

    try:
        assistant_response = await ask_assistant(user_input)
        logger.info(f"Assistant's response: {assistant_response}")

        await message.answer(assistant_response)

    except Exception as e:
        logger.error(f"Error when replying: {e}")
        await message.answer("Sorry, something went wrong. Please try again later.")
