from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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
    BTN_LOW_HIGH_FODMAP,
    BTN_PRODUCT_SEARCH,
    BTN_FODMAP_INFO,
    BTN_BOOK_CONSULTATION,
    BTN_BACK_TO_MAIN_MENU,
    BTN_BACK_TO_CATEGORIES,
    BTN_WHAT_IS_FODMAP,
    BTN_DIET_STAGES,
    BTN_SYMPTOMS_CAUSE,
)
from rapidfuzz import process, fuzz

router = Router()


# --- FSM States ---
class SearchState(StatesGroup):
    waiting_for_product_name = State()


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


@router.message(F.text == BTN_BACK_TO_MAIN_MENU)
async def cmd_back_to_main_menu(message: types.Message):
    await message.answer("Оберіть опцію з меню:", reply_markup=get_main_menu())


# --- КАТЕГОРІЇ ---
@router.message(F.text == BTN_CATEGORIES)
async def cmd_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇", reply_markup=get_product_categories_keyboard()
    )


@router.message(lambda msg: msg.text in CATEGORY_NAME_TO_ID.keys())
async def ask_category(message: types.Message):
    category_id = CATEGORY_NAME_TO_ID[message.text]
    products_keyboard = get_products_keyboard(category_id)

    if products_keyboard:
        await message.answer(
            text=f"Оберіть продукт з категорії {message.text}:",
            reply_markup=products_keyboard,
        )
    else:
        await message.answer("Нажаль, продукти цієї категорії не знайдені.")


@router.message(F.text == BTN_BACK_TO_CATEGORIES)
async def back_to_categories(message: types.Message):
    await message.answer(
        "Оберіть категорію продуктів 👇", reply_markup=get_product_categories_keyboard()
    )


# --- ПРОДУКТИ LOW/HIGH ---
@router.message(Command("fodmap_products"))
async def cmd_fodmap_products(message: types.Message):
    await show_low_high_fodmap_products(message)


@router.message(F.text == BTN_LOW_HIGH_FODMAP)
async def show_low_high_fodmap_products(message: types.Message):
    low_fodmap_products = [
        p["name"] for p in PRODUCTS if p.get("overall_fodmap_level") == "low"
    ]
    high_fodmap_products = [
        p["name"] for p in PRODUCTS if p.get("overall_fodmap_level") == "high"
    ]

    low_list = "\n".join([f"✅ {name}" for name in low_fodmap_products])
    high_list = "\n".join([f"🚫 {name}" for name in high_fodmap_products])

    text = (
        "<b>Продукти з низьким вмістом FODMAP:</b>\n\n"
        f"{low_list}\n\n"
        "<b>Продукти з високим вмістом FODMAP:</b>\n\n"
        f"{high_list}\n\n"
        "❗️ Памʼятайте, FODMAP речовини з різних продуктів можуть накопичуватись.\n\n"
        "👉 <b>Лікую, а не лякаю 🫂</b>"
    )

    await message.answer(text)


# --- INFO ---
@router.message(F.text == BTN_FODMAP_INFO)
async def cmd_fodmap_info(message: types.Message):
    await message.answer(
        "Оберіть, що вас цікавить 👇", reply_markup=get_fodmap_info_keyboard()
    )


@router.message(F.text == BTN_WHAT_IS_FODMAP)
async def explain_fodmap(message: types.Message):
    await message.answer(
        "🥦 <b>Що таке FODMAP?</b>\n\n... (текст залишаємо як раніше) ..."
    )


@router.message(F.text == BTN_DIET_STAGES)
async def explain_diet_steps(message: types.Message):
    await message.answer(
        "📋 <b>Етапи дієти Low-FODMAP</b>\n\n... (текст залишаємо як раніше) ..."
    )


@router.message(F.text == BTN_SYMPTOMS_CAUSE)
async def explain_symptoms(message: types.Message):
    await message.answer(
        "🧐 <b>Чому виникають симптоми?</b>\n\n... (текст залишаємо як раніше) ..."
    )


@router.message(lambda msg: msg.text in [product["name"] for product in PRODUCTS])
async def handle_category_product(message: types.Message):
    product = find_product_by_name(message.text)

    if product:
        await show_product_details(message, product)
    else:
        # Цього не мало би бути, але про всяк випадок
        await message.answer("Продукт не знайдено 😢")


# --- ПОШУК ПРОДУКТУ ---
@router.message(F.text == BTN_PRODUCT_SEARCH)
async def cmd_product_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.waiting_for_product_name)
    await message.answer("Введіть назву продукту для пошуку 🧐")


@router.message(SearchState.waiting_for_product_name)
async def search_product_by_text(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    product = find_product_by_name(user_input) or find_product_by_name_fuzzy(user_input)

    if product:
        await show_product_details(message, product)
    else:
        await message.answer("Продукт не знайдено 😢 Спробуйте інший запит!")
    await state.clear()


# --- fallback + ASSISTANT ---
@router.message()
async def fallback_to_assistant(message: types.Message):
    user_input = message.text.strip()
    msg = await message.reply("👀 Пішов шукати...")

    product_names = [p["name"] for p in PRODUCTS]
    context = (
        "У мене є список продуктів на дієті Low-FODMAP: "
        + ", ".join(product_names)
        + ". Якщо продукту немає в списку, дай загальну відповідь згідно протоколу Low-FODMAP."
    )

    query = (
        f"{context}\n\nКористувач питає про продукт '{user_input}'. "
        "Відповідь має бути відповідно до правил дієти Low-FODMAP, "
        "на основі перевірених джерел Дарʼї Володимирівни."
    )

    response = await ask_assistant(query)
    await msg.delete()
    await message.answer(response)


# --- HELPERS ---
def find_product_by_name(name: str):
    return next((p for p in PRODUCTS if p["name"].lower() == name.lower()), None)


def find_product_by_name_fuzzy(name: str, threshold: int = 80):
    product_names = [p["name"] for p in PRODUCTS]
    match = process.extractOne(name, product_names, scorer=fuzz.WRatio)
    if match and match[1] >= threshold:
        return next((p for p in PRODUCTS if p["name"] == match[0]), None)
    return None


def format_fodmaps(fodmaps: dict) -> str:
    return (
        f"Фруктоза: {fodmaps.get('fructose', '❓')}  "
        f"Лактоза: {fodmaps.get('lactose', '❓')}\n"
        f"Манітол: {fodmaps.get('mannitol', '❓')}  "
        f"Сорбітол: {fodmaps.get('sorbitol', '❓')}\n"
        f"ГОС: {fodmaps.get('gos', '❓')}  "
        f"Фруктани: {fodmaps.get('fructans', '❓')}"
    )


async def show_product_details(message: types.Message, product: dict):
    msg = await message.reply("👀 Пішов шукати...")

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
