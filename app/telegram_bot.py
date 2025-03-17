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

# Inline Query Handler for product search
@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    """
    Handles inline queries from the user.
    User can type @your_bot_name <product> to search for product info.
    """
    # Get the user query from inline search input
    query = inline_query.query.strip().lower()

    # If no query, return empty result to avoid unnecessary processing
    if not query:
        return await inline_query.answer([], cache_time=1)

    # Prepare prompt to send to OpenAI Assistant
    prompt = (
        f"Надай інформацію про продукт '{query}' згідно дієти Low-FODMAP. "
        "Форматуй відповідь як завжди: статус, дози, пояснення, поради gastroкоуча Дарʼї Володимирівни."
    )

    # Get the assistant's response from Assistants API
    response = await ask_assistant(prompt)

    # Build the InlineQueryResultArticle to show in inline search
    results = [
        types.InlineQueryResultArticle(
            id="1",  # Must be unique. If looping multiple results, use unique id.
            title=f"Інформація про {query.capitalize()}",
            description="Натисніть, щоб отримати інформацію про продукт",
            input_message_content=types.InputTextMessageContent(
                message_text=response  # What will be sent in chat on click
            )
        )
    ]

    # Answer the inline query with the prepared results
    await inline_query.answer(results, cache_time=5)

