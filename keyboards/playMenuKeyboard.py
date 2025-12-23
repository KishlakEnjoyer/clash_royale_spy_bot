from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

host_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='▶️ Запустить раунд', callback_data='start_round')],
    [InlineKeyboardButton(text='🚪 Выйти из комнаты', callback_data='leave_room')]
])



player_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚪 Выйти из комнаты', callback_data='leave_room')]
])