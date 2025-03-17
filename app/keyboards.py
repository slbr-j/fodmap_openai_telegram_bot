from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PRODUCT_CATEGORIES_ROWS = [
    ["🍞 Хлібобулочні вироби", "🥦 Овочі"],
    ["🍓 Фрукти", "🥛 Молочні, безлактозні продукти"],
    ["🥜 Бобові, горіхи, тофу", "🍹 Напої"],
    ["🥩 М'ясо, риба, яйця", "🧈 Жири та масла"],
    ["🧂 Спеції, соуси", "🍪 Снеки, батончики, печиво"],
    ["🍰 Кондитерські вироби, цукор"]
]

PRODUCT_CATEGORIES = [item for row in PRODUCT_CATEGORIES_ROWS for item in row]

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
    keyboard = [
        [KeyboardButton(text=label) for label in row]
        for row in PRODUCT_CATEGORIES_ROWS
    ]
    keyboard.append([KeyboardButton(text="🔙 Назад до головного меню")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_next_actions_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Дивитися інші овочі", callback_data="category_ovochi_next")],
        [InlineKeyboardButton(text="🔙 Назад до категорій", callback_data="back_to_categories")]
    ])
    return keyboard
