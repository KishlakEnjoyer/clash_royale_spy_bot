from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆕 Создать комнату', callback_data='create_room')],
    [InlineKeyboardButton(text='🌐 Присоединиться к комнате', callback_data='join_room')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back')]
])