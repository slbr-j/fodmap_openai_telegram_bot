from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Консультація", callback_data="consult")],
            [InlineKeyboardButton(text="📄 Поради", callback_data="tips")],
            [InlineKeyboardButton(text="❓ FAQ", callback_data="faq")],
        ]
    )
    return keyboard
