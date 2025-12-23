from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_show_keyboard(role: str, card_name: str = ""):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать", callback_data=f"show_card:{role}:{card_name}")]
    ])

def get_hide_keyboard(role: str, card_name: str = ""):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скрыть", callback_data=f"hide_card:{role}:{card_name}")]
    ])