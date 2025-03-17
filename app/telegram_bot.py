from aiogram import Router, types
from aiogram.filters import Command
from keyboards import get_main_menu, get_product_categories_keyboard
import json

router = Router()

# Завантаження бази продуктів із JSON
with open("data/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Пошук продуктів
def search_products_by_category(category):
    return [prod for prod in products if prod["категорія"] == category]

def search_product_by_name(name):
    for prod in products:
        if prod["назва"].lower() == name.lower():
            return prod
    return None

# Форматування відповіді по продукту
def format_product_info(product):
    return (
        f"🔸 {product['назва']}\n"
        f"{product['статус']}\n\n"
        f"✅ Безпечна доза: {product['доза_безпечна']}\n"
        f"⚠️ Потенційно небезпечна доза: {product['доза_небезпечна']}\n\n"
        f"FODMAP профіль:\n"
        f"Фруктоза {product['фруктоза']}\n"
        f"Лактоза {product['лактоза']}\n"
        f"Манітол {product['манітол']}\n"
        f"Сорбітол {product['сорбітол']}\n\n"
        f"📌 Порада gastroкоуча Дарʼї Володимирівни:\n"
        f"{product['коментар']}\n\n"
        f"Лікую, а не лякаю 🫂"
    )

# Команди /start і Головне меню
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
async def show_products_in_category(message: types.Message):
    category = message.text.replace("🍓 ", "").replace("🥦 ", "").replace("🥛 ", "").replace("🍹 ", "").replace("🍞 ", "").replace("🥜 ", "").replace("🥩 ", "").replace("🧈 ", "").replace("🍪 ", "").replace("🍰 ", "").replace("🧂 ", "")
    category_products = search_products_by_category(category)

    if not category_products:
        await message.answer("Немає продуктів у цій категорії 😕")
        return

    # Показуємо список продуктів
    product_names = [prod["назва"] for prod in category_products]
    products_list = "\n".join([f"🔸 {name}" for name in product_names])

    await message.answer(f"Продукти в категорії {category}:\n\n{products_list}\n\nВведіть назву продукту, щоб дізнатися деталі.")

# ПОШУК ПРОДУКТІВ
@router.message(lambda msg: msg.text == "🥦 Продукти (пошук)")
async def cmd_product_search(message: types.Message):
    await message.answer("Введіть назву продукту для пошуку 🧐")

@router.message()
async def search_product_handler(message: types.Message):
    user_input = message.text.strip()

    product = search_product_by_name(user_input)

    if product:
        product_info = format_product_info(product)
        await message.answer(product_info)
    else:
        await message.answer("Не знайшов такого продукту 😕\n\nСпробуй ще раз або обери категорію з меню.")

# ЗАПИС НА КОНСУЛЬТАЦІЮ
@router.message(lambda msg: msg.text == "📅 Записатись на консультацію")
async def cmd_consultation(message: types.Message):
    await message.answer(
        "Дарʼя Володимирівна консультує в клініці Vita Medical.\n\n"
        "Запис через сайт: https://vitamedical.com.ua/\n"
        "Або через телеграм бот клініки: https://t.me/vitamedicalBot\n\n"
        "Не консультую в Direct! Google 24/7 — go! 😉"
    )
