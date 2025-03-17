from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    keyboard = [
        [KeyboardButton(text="🍎 Категорії продуктів")],
        [KeyboardButton(text="🥦 Продукти (пошук)")],
        [KeyboardButton(text="📅 Записатись на консультацію")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

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
