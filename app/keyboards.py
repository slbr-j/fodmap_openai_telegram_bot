from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_loader import CATEGORIES, CATEGORY_ID_TO_NAME, get_products_by_category
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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


def get_main_menu():
    keyboard = [
        [KeyboardButton(text=BTN_CATEGORIES)],
        [KeyboardButton(text=BTN_LOW_HIGH_FODMAP)],
        [KeyboardButton(text=BTN_PRODUCT_SEARCH)],
        [KeyboardButton(text=BTN_FODMAP_INFO)],
        [KeyboardButton(text=BTN_BOOK_CONSULTATION)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,  # адаптує розмір кнопок
        one_time_keyboard=False,  # кнопки залишаються завжди на екрані
        input_field_placeholder="Оберіть опцію з меню 👇",  # текст підказки
    )


def get_fodmap_info_keyboard():
    keyboard = [
        [KeyboardButton(text=BTN_WHAT_IS_FODMAP)],
        [KeyboardButton(text=BTN_DIET_STAGES)],
        [KeyboardButton(text=BTN_SYMPTOMS_CAUSE)],
        [KeyboardButton(text=BTN_BOOK_CONSULTATION)],
        [KeyboardButton(text=BTN_BACK_TO_MAIN_MENU)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


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
    keyboard_rows.append([KeyboardButton(text=BTN_BACK_TO_MAIN_MENU)])

    return ReplyKeyboardMarkup(keyboard=keyboard_rows, resize_keyboard=True)


def get_products_keyboard(category_id: str):
    """
    Генерує клавіатуру продуктів певної категорії.
    """
    products = get_products_by_category(category_id)

    if not products:
        return None

    keyboard = []
    row = []
    for idx, product in enumerate(products, 1):
        row.append(KeyboardButton(text=product["name"]))
        if idx % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Додаємо кнопку "Назад до категорій"
    keyboard.append([KeyboardButton(text=BTN_BACK_TO_CATEGORIES)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_next_actions_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Дивитися інші овочі", callback_data="category_ovochi_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BTN_BACK_TO_CATEGORIES, callback_data="back_to_categories"
                )
            ],
        ]
    )
    return keyboard
