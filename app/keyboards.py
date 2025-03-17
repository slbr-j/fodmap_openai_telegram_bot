from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="📋 Часті питання")],
        [KeyboardButton(text="🍏 Категорії продуктів")],
        [KeyboardButton(text="📅 Записатися на консультацію")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
