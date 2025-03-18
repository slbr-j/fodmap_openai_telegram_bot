from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ChatAction
from keyboards import get_main_menu, get_product_categories_keyboard, get_products_keyboardб get_fodmap_info_keyboard
from data_loader import CATEGORIES, CATEGORY_NAME_TO_ID, CATEGORY_ID_TO_NAME, PRODUCTS, get_products_by_category
from assistants_api import ask_assistant
from keyboard_labels import (
    BTN_CATEGORIES,
    BTN_PRODUCT_SEARCH,
    BTN_FODMAP_INFO,
    BTN_BOOK_CONSULTATION,
    BTN_BACK_TO_MAIN_MENU,
    BTN_BACK_TO_CATEGORIES,
    BTN_WHAT_IS_FODMAP,
    BTN_DIET_STAGES,
    BTN_SYMPTOMS_CAUSE
)

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
@router.message(lambda msg: msg.text == BTN_BOOK_CONSULTATION)
async def cmd_consultation(message: types.Message):
    # Показуємо що "друкує"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    await message.answer(
        "Дарʼя Володимирівна консультує в клініці Vita Medical.\n\n"
        "Запис через сайт: https://vitamedical.com.ua/\n"
        "Або через телеграм бот клініки: https://t.me/vitamedicalBot\n\n"
        "Не консультую в Direct! Google 24/7 — go! 😉"
    )
# ABOUT FODMAP
@router.message(lambda msg: msg.text == BTN_FODMAP_INFO)
async def cmd_fodmap_info(message: types.Message):
    await message.answer(
        "Оберіть, що вас цікавить 👇",
        reply_markup=get_fodmap_info_keyboard()
    )

@router.message(lambda msg: msg.text == BTN_WHAT_IS_FODMAP)
async def explain_fodmap(message: types.Message):
    await message.answer(
        "🥦 **Що таке FODMAP?**\n\n"
        "FODMAP — це група вуглеводів, які погано засвоюються у тонкому кишечнику.\n"
        "Вони можуть викликати здуття живота, біль, діарею та газоутворення.\n\n"
        "**До FODMAP належать:**\n"
        "- **Фруктоза** (🍯 мед, фрукти)\n"
        "- **Лактоза** (🥛 молочні продукти)\n"
        "- **Поліоли** (🍬 сорбітол, манітол)\n"
        "- **Фруктани та ГЗК** (🧄 цибуля, часник, бобові)\n\n"
        "👉 **Лікую, а не лякаю 🫂**"
    )

@router.message(lambda msg: msg.text == BTN_DIET_STAGES)
async def explain_diet_steps(message: types.Message):
    await message.answer(
        "📋 **Етапи дієти Low-FODMAP**\n\n"
        "1️⃣ **Елімінація (2-6 тижнів):**\n"
        "Виключаємо продукти з високим вмістом FODMAP.\n\n"
        "2️⃣ **Реінтродукція (6-8 тижнів):**\n"
        "Повертаємо продукти по черзі, перевіряючи реакцію організму.\n\n"
        "3️⃣ **Персоналізація:**\n"
        "Формуємо свій раціон, уникаючи лише проблемні FODMAP.\n\n"
        "👉 **Лікую, а не лякаю 🫂**"
    )

@router.message(lambda msg: msg.text == BTN_SYMPTOMS_CAUSE)
async def explain_symptoms(message: types.Message):
    await message.answer(
        "🧐 **Чому виникають симптоми?**\n\n"
        "FODMAP притягують воду в кишківник 💧 та ферментуються бактеріями 🦠, "
        "що спричиняє:\n"
        "- здуття 🎈\n"
        "- біль 🥴\n"
        "- діарею 🚽\n\n"
        "Особливо це актуально для людей із синдромом подразненого кишечника (IBS), "
        "бо їх кишківник більш чутливий.\n\n"
        "👉 **Лікую, а не лякаю 🫂**"
    )


# Назад до головного меню
@router.message(lambda msg: msg.text == BTN_BACK_TO_MAIN_MENU)
async def cmd_back_to_main_menu(message: types.Message):
    await message.answer(
        "Оберіть опцію з меню 👇",
        reply_markup=get_main_menu()
    )

# КАТЕГОРІЇ
@router.message(lambda msg: msg.text == BTN_CATEGORIES)
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

@router.message(lambda msg: msg.text == BTN_BACK_TO_CATEGORIES)
async def back_to_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇",
        reply_markup=get_product_categories_keyboard()
    )

def find_product_by_name(name: str):
    """
    Повертає продукт з PRODUCTS за його name.
    Пошук нечутливий до регістру.
    """
    return next((p for p in PRODUCTS if p["name"].lower() == name.lower()), None)

def format_fodmaps(fodmaps: dict) -> str:
    """
    Форматує FODMAP значення в красивий рядок.
    """
    return (
        f"Фруктоза: {fodmaps.get('fructose', '❓')}  "
        f"Лактоза: {fodmaps.get('lactose', '❓')}\n"
        f"Манітол: {fodmaps.get('mannitol', '❓')}  "
        f"Сорбітол: {fodmaps.get('sorbitol', '❓')}\n"
        f"ГОС: {fodmaps.get('gos', '❓')}  "
        f"Фруктани: {fodmaps.get('fructans', '❓')}"
    )


@router.message(lambda msg: msg.text in [product["name"] for product in PRODUCTS])
async def show_product_info(message: types.Message):
    # Пошук продукту за ім'ям
    product = next((p for p in PRODUCTS if p["name"] == message.text), None)

    if not product:
        await message.answer("Продукт не знайдено 😢")
        return

    msg = await message.reply("👀 Пішов шукати...")

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Витягуємо дані доз
    low_dose = product['doses']['low']
    moderate_dose = product['doses']['moderate']
    high_dose = product['doses']['high']

    # Формуємо відповідь про продукт
    text = (
        f"📝 <b>{product['name']}</b>\n"
        f"Статус: {product['status']}\n\n"

        f"🟢 <b>Безпечна доза</b>: {low_dose['amount']}\n"
        f"{format_fodmaps(low_dose['fodmaps'])}\n\n"

        f"🟡 <b>Помірна доза</b>: {moderate_dose['amount']}\n"
        f"{format_fodmaps(moderate_dose['fodmaps'])}\n\n"

        f"🔴 <b>Небезпечна доза</b>: {high_dose['amount']}\n"
        f"{format_fodmaps(high_dose['fodmaps'])}\n\n"

        f"{product.get('comment', '')}\n\n"
        f"❗️ Памʼятайте, що FODMAP речовини можуть накопичуватись при комбінації продуктів.\n\n"
        f"👉 Лікую, а не лякаю 🫂"
    )

    await msg.delete()

    await message.answer(text, parse_mode="HTML")


# ПОШУК ПРОДУКТУ
@router.message(lambda msg: msg.text == BTN_PRODUCT_SEARCH)
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")

@router.message()
async def ask_product_info(message: types.Message):
    user_input = message.text.strip()

    # Перевіряємо, чи є продукт у PRODUCTS
    product = find_product_by_name(user_input)
    if product:
        return await show_product_info(message, product)

    # Якщо продукт не знайдений, йдемо до ассистента
    msg = await message.reply("👀 Пішов шукати...")

    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    query = f"Розкажи про продукт '{user_input}' згідно дієти Low-FODMAP. Використовуй дані з завантаженого файлу."

    response = await ask_assistant(query)
    
    await msg.delete()
    await message.answer(response)
