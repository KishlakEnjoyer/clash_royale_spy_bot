from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart

from keyboards import contactsKeyboard as kb
import storage as st

router = Router()

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    """
    Просто вывод информации
    """
    await message.answer(f'Привет,{message.from_user.first_name}!' +
            '\nЭто бот для игры в шпиона по тематике Clash Royale!' +
            '\nДля начала игры: /play' +
            '\nКонтакты разработчика ⬇️', reply_markup=kb.contacts)