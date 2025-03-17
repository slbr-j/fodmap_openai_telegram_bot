from aiogram import Router, types
from aiogram.filters import Command
from keyboards import get_main_menu, get_product_categories_keyboard
from assistants_api import ask_assistant

router = Router()

# Старт / Головне меню
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я FODMAP асистент 👩🏻‍⚕️\n\nОберіть опцію з меню:",
        reply_markup=get_main_menu()
    )

@router.message(lambda msg: msg.text == "📋 Головне меню")
async def cmd_menu(message: types.Message):
    await message.answer("Оберіть опцію з меню:", reply_markup=get_main_menu())

# КАТЕГОРІЇ
@router.message(lambda msg: msg.text == "🍎 Категорії продуктів")
async def cmd_categories(message: types.Message):
    await message.answer("Оберіть категорію продуктів:", reply_markup=get_product_categories_keyboard())

@router.message(lambda msg: msg.text in [
    "🍓 Фрукти", "🥦 Овочі", "🥛 Молочні, безлактозні продукти",
    "🍹 Напої", "🥜 Бобові, горіхи, тофу", "🥩 М'ясо, риба, яйця",
    "🧈 Жири та масла", "🍪 Снеки, батончики, печиво", "🍰 Кондитерські вироби, цукор",
    "🧂 Спеції, соуси", "🍞 Хлібобулочні вироби"
])
async def ask_category(message: types.Message):
    category_name = message.text.replace("🍓 ", "").replace("🥦 ", "")  # прибираємо emoji
    query = f"Покажи всі продукти з категорії '{category_name}' відповідно до FODMAP."

    # Асистент генерує відповідь на запит
    response = await ask_assistant(query)

    await message.answer(response)

# ПОШУК ПРОДУКТУ
@router.message(lambda msg: msg.text == "🥦 Продукти (пошук)")
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")

@router.message()
async def ask_product_info(message: types.Message):
    user_input = message.text.strip()

    # List of static button responses that are already handled above
    IGNORED_BUTTONS = [
        "📅 Записатись на консультацію",
        "📋 Головне меню",
        "🍎 Категорії продуктів",
        "🥦 Продукти (пошук)",
        "🍓 Фрукти", "🥦 Овочі", "🥛 Молочні, безлактозні продукти",
        "🍹 Напої", "🥜 Бобові, горіхи, тофу", "🥩 М'ясо, риба, яйця",
        "🧈 Жири та масла", "🍪 Снеки, батончики, печиво",
        "🍰 Кондитерські вироби, цукор", "🧂 Спеції, соуси", "🍞 Хлібобулочні вироби"
    ]

    # If message is in ignored buttons, do nothing (already handled)
    if user_input in IGNORED_BUTTONS:
        return

    # Otherwise, send the query to OpenAI Assistant
    query = f"Розкажи про продукт '{user_input}' згідно дієти Low-FODMAP. Використовуй дані з завантаженого файлу."

    response = await ask_assistant(query)

    await message.answer(response)


# ЗАПИС НА КОНСУЛЬТАЦІЮ
@router.message(lambda msg: msg.text == "📅 Записатись на консультацію")
async def cmd_consultation(message: types.Message):
    await message.answer(
        "Дарʼя Володимирівна консультує в клініці Vita Medical.\n\n"
        "Запис через сайт: https://vitamedical.com.ua/\n"
        "Або через телеграм бот клініки: https://t.me/vitamedicalBot\n\n"
        "Не консультую в Direct! Google 24/7 — go! 😉"
    )
