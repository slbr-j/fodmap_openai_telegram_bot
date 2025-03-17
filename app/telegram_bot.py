from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ChatActions
from keyboards import get_main_menu, get_product_categories_keyboard, PRODUCT_CATEGORIES
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

# ЗАПИС НА КОНСУЛЬТАЦІЮ
@router.message(lambda msg: msg.text == "📅 Записатись на консультацію")
async def cmd_consultation(message: types.Message):
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
@router.message(lambda msg: msg.text in PRODUCT_CATEGORIES.keys())
async def ask_category(message: types.Message):
    # Отримуємо значення з PRODUCT_CATEGORIES словника
    category_key = PRODUCT_CATEGORIES[message.text]

    query = f"Покажи всі продукти з категорії '{category_key}' відповідно до FODMAP."

    response = await ask_assistant(query)

    await message.answer(response)

# ПОШУК ПРОДУКТУ
@router.message(lambda msg: msg.text == "🥦 Продукти (пошук)")
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")

@router.message()
async def ask_product_info(message: types.Message):
    user_input = message.text.strip()
    msg = await message.reply("👀 Шукаю інформацію...")
    # Показуємо що "друкує"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatActions.TYPING)

    # Готуємо запит до асистента
    query = f"Розкажи про продукт '{user_input}' згідно дієти Low-FODMAP. Використовуй дані з завантаженого файлу."

    # Викликаємо асистента
    response = await ask_assistant(query)
    
    # Видаляємо тимчасове повідомлення
    await msg.delete()

    # Відповідь користувачу
    await message.answer(response)
