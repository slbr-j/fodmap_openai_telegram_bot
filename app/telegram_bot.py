from aiogram import types, Router
from aiogram.filters import Command
from assistants_api import ask_assistant
from keyboards import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.answer(
        "Привіт! Я FODMAP асистент👩🏻‍⚕️\n\nЯк можу допомогти?",
        reply_markup=get_main_keyboard(),
    )

@router.message()
async def handle_text(message: types.Message):
    user_input = message.text
    logger.info(f"User {message.from_user.id} asked: {user_input}")

    try:
        assistant_response = await ask_assistant(user_input)
        logger.info(f"Assistant response: {assistant_response}")

        await message.answer(assistant_response)

    except Exception as e:
        logger.error(f"Error in handle_text: {e}")
        await message.answer("Вибач, сталася помилка. Спробуй ще раз пізніше 🙏")
