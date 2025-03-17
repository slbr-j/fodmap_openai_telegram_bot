from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_loader import CATEGORIES, PRODUCTS, get_products_by_category
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = [
        [KeyboardButton(text="🍎 Категорії продуктів")],
        [KeyboardButton(text="🥦 Продукти (пошук)")],
        [KeyboardButton(text="📅 Записатись на консультацію")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,       # адаптує розмір кнопок
        one_time_keyboard=False,    # кнопки залишаються завжди на екрані
        input_field_placeholder="Оберіть опцію з меню 👇"  # текст підказки
    )
    
def get_product_categories_keyboard():
    keyboard_rows = []
    row = []

    for idx, category in enumerate(CATEGORIES, start=1):
        btn_text = f"{category['emoji']} {category['name']}"
        row.append(KeyboardButton(text=btn_text))

        # Дві кнопки в рядку
        if idx % 2 == 0 or idx == len(CATEGORIES):
            keyboard_rows.append(row)
            row = []

    # Кнопка "Назад"
    keyboard_rows.append([KeyboardButton(text="🔙 Назад до головного меню")])

    return ReplyKeyboardMarkup(keyboard=keyboard_rows, resize_keyboard=True)

def get_next_actions_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Дивитися інші овочі", callback_data="category_ovochi_next")],
        [InlineKeyboardButton(text="🔙 Назад до категорій", callback_data="back_to_categories")]
    ])
    return keyboard
