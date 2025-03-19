from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ChatAction
import re
from keyboards import (
    get_main_menu,
    get_product_categories_keyboard,
    get_products_keyboard,
    get_fodmap_info_keyboard,
)
from data_loader import (
    CATEGORIES,
    CATEGORY_NAME_TO_ID,
    CATEGORY_ID_TO_NAME,
    PRODUCTS,
    get_products_by_category,
)
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
    BTN_SYMPTOMS_CAUSE,
)

router = Router()

BOOKING_KEYWORDS = [
    r"\bзапис(атись|атися)?\b",
    r"\bконсультац(ія|ії|ію|іями)?\b",
    r"\bпроконсульту(є|ватись|ватися)?\b",
    r"\bappointment\b",
    r"\bbook\b",
    r"\bschedule\b",
]


@router.message(
    lambda msg: any(
        re.search(pattern, msg.text.lower()) for pattern in BOOKING_KEYWORDS
    )
)
async def auto_consultation(message: types.Message):
    await message.answer(
        "Дарʼя Володимирівна Помазан не проводить консультацій у Direct або в цьому чаті.\n\n"
        "Всі консультації призначаються через офіційні канали клініки Vita Medical.\n\n"
        "➡️ <a href='https://vitamedical.com.ua/'>vitamedical.com.ua</a>\n"
        "➡️ <a href='https://t.me/vitamedicalBot'>t.me/vitamedicalBot</a>\n\n"
        "❗️ Не соромтесь записуватись, ваше здоров’я важливе!\n\n"
        "👉 <b>Лікую, а не лякаю 🫂</b>"
    )


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )
    await message.answer(
        "Привіт! \n\nОберіть опцію з меню:",
        reply_markup=get_main_menu(),
    )


@router.message(lambda msg: msg.text == "📋 Головне меню")
async def cmd_menu(message: types.Message):
    await message.answer("Оберіть опцію з меню:", reply_markup=get_main_menu())


# BOOKING
@router.message(lambda msg: msg.text == BTN_BOOK_CONSULTATION)
async def cmd_consultation(message: types.Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )
    await message.answer(
        "Дарʼя Володимирівна консультує в клініці Vita Medical.\n\n"
        "Запис через сайт: <a href='https://vitamedical.com.ua/'>vitamedical.com.ua</a>\n"
        "Або через телеграм бот клініки: <a href='https://t.me/vitamedicalBot'>t.me/vitamedicalBot</a>\n\n"
        "Не консультую в Direct! Google 24/7 — go! 😉"
    )


# ABOUT FODMAP
@router.message(lambda msg: msg.text == BTN_FODMAP_INFO)
async def cmd_fodmap_info(message: types.Message):
    await message.answer(
        "Оберіть, що вас цікавить 👇", reply_markup=get_fodmap_info_keyboard()
    )


@router.message(lambda msg: msg.text == BTN_WHAT_IS_FODMAP)
async def explain_fodmap(message: types.Message):
    await message.answer(
        "🥦 <b>Що таке FODMAP?</b>\n\n"
        "<b>FODMAP</b> — це абревіатура від:\n\n"
        "• <b>F</b>ermentable — Ферментовані\n"
        "• <b>O</b>ligosaccharides — Олігосахариди (фруктани, ГЗК)\n"
        "• <b>D</b>isaccharides — Дисахариди (лактоза)\n"
        "• <b>M</b>onosaccharides — Монозахариди (фруктоза)\n"
        "• <b>A</b>nd — та\n"
        "• <b>P</b>olyols — Поліоли (сорбітол, манітол)\n\n"
        "Це група вуглеводів, які погано засвоюються у тонкому кишечнику.\n\n"
        "Вони можуть викликати:\n"
        "🔹 здуття живота\n"
        "🔹 біль\n"
        "🔹 діарею\n"
        "🔹 газоутворення\n\n"
        "<b>До FODMAP належать:</b>\n\n"
        "🍯 <b>Фруктоза</b> — мед, деякі фрукти\n"
        "🥛 <b>Лактоза</b> — молочні продукти\n"
        "🍬 <b>Поліоли</b> — сорбітол, манітол\n"
        "🧄 <b>Фруктани та ГЗК</b> — цибуля, часник, бобові\n\n"
        "👉 <b>Лікую, а не лякаю 🫂</b>"
    )


@router.message(lambda msg: msg.text == BTN_DIET_STAGES)
async def explain_diet_steps(message: types.Message):
    await message.answer(
        "📋 <b>Етапи дієти Low-FODMAP</b>\n\n"
        "1️⃣ <b>Елімінація (2-6 тижнів):</b>\n"
        "Виключаємо продукти з високим вмістом FODMAP.\n\n"
        "2️⃣ <b>Реінтродукція (6-8 тижнів):</b>\n"
        "Повертаємо продукти по черзі, перевіряючи реакцію організму.\n\n"
        "3️⃣ <b>Персоналізація:</b>\n"
        "Формуємо свій раціон, уникаючи лише проблемні FODMAP.\n\n"
        "👉 <b>Лікую, а не лякаю 🫂</b>"
    )


@router.message(lambda msg: msg.text == BTN_SYMPTOMS_CAUSE)
async def explain_symptoms(message: types.Message):
    await message.answer(
        "🧐 <b>Чому виникають симптоми?</b>\n\n"
        "FODMAP притягують воду в кишківник 💧 та ферментуються бактеріями 🦠, що спричиняє:\n\n"
        "🔹 здуття 🎈\n"
        "🔹 біль 🥴\n"
        "🔹 діарею 🚽\n\n"
        "Особливо це актуально для людей із синдромом подразненого кишечника (IBS).\n\n"
        "👉 <b>Лікую, а не лякаю 🫂</b>"
    )


# Назад до головного меню
@router.message(lambda msg: msg.text == BTN_BACK_TO_MAIN_MENU)
async def cmd_back_to_main_menu(message: types.Message):
    await message.answer("Оберіть опцію з меню 👇", reply_markup=get_main_menu())


# КАТЕГОРІЇ
@router.message(lambda msg: msg.text == BTN_CATEGORIES)
async def cmd_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇", reply_markup=get_product_categories_keyboard()
    )


# Обробка категорій за текстом кнопки
@router.message(lambda msg: msg.text in CATEGORY_NAME_TO_ID.keys())
async def ask_category(message: types.Message):
    category_id = CATEGORY_NAME_TO_ID[message.text]

    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )

    products_keyboard = get_products_keyboard(category_id)

    if products_keyboard:
        await message.answer(
            text=f"Оберіть продукт з категорії {message.text}:",
            reply_markup=products_keyboard,
        )
    else:
        await message.answer("Нажаль, продукти цієї категорії не знайдені.")


@router.message(lambda msg: msg.text == BTN_BACK_TO_CATEGORIES)
async def back_to_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇", reply_markup=get_product_categories_keyboard()
    )


# Пошук продукту
def find_product_by_name(name: str):
    return next((p for p in PRODUCTS if p["name"].lower() == name.lower()), None)


def format_fodmaps(fodmaps: dict) -> str:
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
    product = find_product_by_name(message.text)

    if not product:
        await message.answer("Продукт не знайдено 😢")
        return

    msg = await message.reply("👀 Пішов шукати...")

    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )

    low_dose = product["doses"]["low"]
    moderate_dose = product["doses"]["moderate"]
    high_dose = product["doses"]["high"]

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
    await message.answer(text)


# ПОШУК ПРОДУКТУ
@router.message(lambda msg: msg.text == BTN_PRODUCT_SEARCH)
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")


@router.message()
async def ask_product_info(message: types.Message):
    user_input = message.text.strip()

    product = find_product_by_name(user_input)
    if product:
        return await show_product_info(message)

    msg = await message.reply("👀 Пішов шукати...")
    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )

    query = f"Розкажи про продукт '{user_input}' згідно дієти Low-FODMAP. Використовуй дані з завантаженого файлу."
    response = await ask_assistant(query)

    await msg.delete()
    await message.answer(response)
