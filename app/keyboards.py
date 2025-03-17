from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
    keyboard = [
        [KeyboardButton(text="🍞 Хлібобулочні вироби"), KeyboardButton(text="🥦 Овочі")],
        [KeyboardButton(text="🍓 Фрукти"), KeyboardButton(text="🥛 Молочні, безлактозні продукти")],
        [KeyboardButton(text="🥜 Бобові, горіхи, тофу"), KeyboardButton(text="🍹 Напої")],
        [KeyboardButton(text="🥩 М'ясо, риба, яйця"), KeyboardButton(text="🧈 Жири та масла")],
        [KeyboardButton(text="🧂 Спеції, соуси"), KeyboardButton(text="🍪 Снеки, батончики, печиво")],
        [KeyboardButton(text="🍰 Кондитерські вироби, цукор")],
        [KeyboardButton(text="🔙 Назад до головного меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_next_actions_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Дивитися інші овочі", callback_data="category_ovochi_next")],
        [InlineKeyboardButton(text="🔙 Назад до категорій", callback_data="back_to_categories")]
    ])
    return keyboard
