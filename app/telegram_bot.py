from aiogram import types, Router
from aiogram.filters import Command
from assistants_api import ask_assistant
from keyboards import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я FODMAP асистент👩🏻‍⚕️\n\nЯк можу допомогти?",
        reply_markup=get_main_keyboard(),
    )


@router.message()
async def handle_text(message: types.Message):
    user_input = message.text
    assistant_response = await ask_assistant(user_input)
    await message.answer(assistant_response)


from main import dp

dp.include_router(router)
