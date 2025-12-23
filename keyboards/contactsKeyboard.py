from aiogram import Router, types, F
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.filters import Command, CommandStart

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='GitHub', url='https://github.com/KishlakEnjoyer')],
    [InlineKeyboardButton(text='Telegram', url='https://t.me/jdm_enjoyerr')]
])

