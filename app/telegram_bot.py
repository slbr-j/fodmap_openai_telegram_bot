from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ChatAction
from keyboards import get_main_menu, get_product_categories_keyboard, get_products_keyboard
from data_loader import CATEGORIES, CATEGORY_NAME_TO_ID, CATEGORY_ID_TO_NAME, PRODUCTS, get_products_by_category
from assistants_api import ask_assistant

router = Router()

# Старт / Головне меню
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Показуємо що "друкує"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await message.answer(
        "Привіт! Я FODMAP асистент 👩🏻‍⚕️\n\nОберіть опцію з меню:",
        reply_markup=get_main_menu()
    )

@router.message(lambda msg: msg.text == "📋 Головне меню")
async def cmd_menu(message: types.Message):
    await message.answer("Оберіть опцію з меню:", reply_markup=get_main_menu())

# ЗАПИС НА КОНСУЛЬТАЦІЮ
@router.message(lambda msg: msg.text == "📅 Записатись на консультацію")
async def cmd_consultation(message: types.Message):
    # Показуємо що "друкує"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await message.answer(
        "Дарʼя Володимирівна консультує в клініці Vita Medical.\n\n"
        "Запис через сайт: https://vitamedical.com.ua/\n"
        "Або через телеграм бот клініки: https://t.me/vitamedicalBot\n\n"
        "Не консультую в Direct! Google 24/7 — go! 😉"
    )

# Назад до головного меню
@router.message(lambda msg: msg.text == "🔙 Назад до головного меню")
async def cmd_back_to_main_menu(message: types.Message):
    await message.answer(
        "Оберіть опцію з меню 👇",
        reply_markup=get_main_menu()
    )

# КАТЕГОРІЇ
@router.message(lambda msg: msg.text == "🍎 Категорії продуктів")
async def cmd_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇",
        reply_markup=get_product_categories_keyboard()
    )

# Обробка категорій за текстом кнопки
@router.message(lambda msg: msg.text in CATEGORY_NAME_TO_ID.keys())
async def ask_category(message: types.Message):
    category_id = CATEGORY_NAME_TO_ID[message.text]
    
    # Додаємо індикатор, що бот "друкує"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Генеруємо клавіатуру продуктів цієї категорії
    products_keyboard = get_products_keyboard(category_id)

    if products_keyboard:
        await message.answer(
            text=f"Оберіть продукт з категорії {message.text}:",
            reply_markup=products_keyboard
        )
    else:
        await message.answer("Нажаль, продукти цієї категорії не знайдені.")

@router.message(lambda msg: msg.text == "🔙 Назад до категорій")
async def back_to_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇",
        reply_markup=get_product_categories_keyboard()
    )

@router.message(lambda msg: msg.text in [product["name"] for product in PRODUCTS])
async def show_product_info(message: types.Message):
    # Пошук продукту за ім'ям
    product = next((p for p in PRODUCTS if p["name"] == message.text), None)

    if not product:
        await message.answer("Продукт не знайдено 😢")
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Формуємо відповідь про продукт
    text = (
        f"{product['name']}\n"
        f"Статус: {product['status']}\n\n"
        f"🟢 Безпечна доза: {product['doses']['low']}\n"
        f"🟡 Помірна доза: {product['doses']['moderate']}\n"
        f"🔴 Небезпечна доза: {product['doses']['high']}\n\n"
        f"FODMAP речовини:\n"
        f"- Фруктоза: {product['fodmaps'].get('fructose', '❓')}\n"
        f"- Лактоза: {product['fodmaps'].get('lactose', '❓')}\n"
        f"- Манітол: {product['fodmaps'].get('mannitol', '❓')}\n"
        f"- Сорбітол: {product['fodmaps'].get('sorbitol', '❓')}\n"
        f"- ГЗК (GOS): {product['fodmaps'].get('gos', '❓')}\n"
        f"- Фруктани: {product['fodmaps'].get('fructans', '❓')}\n\n"
        f"{product.get('comment', '')}\n\n"
        f"👉 Лікую, а не лякаю 🫂"
    )

    await message.answer(text)

# ПОШУК ПРОДУКТУ
@router.message(lambda msg: msg.text == "🥦 Продукти (пошук)")
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")

@router.message()
async def ask_product_info(message: types.Message):
    user_input = message.text.strip()

    # Перевіряємо, чи є продукт у PRODUCTS
    product = next((p for p in PRODUCTS if p["name"].lower() == user_input.lower()), None)
    
    if product:
        return await show_product_info(message)  # Використовуємо вже готовий хендлер

    # Якщо продукт не знайдений, йдемо до ассистента
    msg = await message.reply("👀 Шукаю інформацію...")

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    query = f"Розкажи про продукт '{user_input}' згідно дієти Low-FODMAP. Використовуй дані з завантаженого файлу."

    response = await ask_assistant(query)
    
    await msg.delete()
    await message.answer(response)
