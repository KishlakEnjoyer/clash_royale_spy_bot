from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile
from aiogram.types import InputMediaPhoto
import os


import storage as st
import game_logic as gl
import keyboards.mainKeyboard as kb
import keyboards.visibilityKeyboard as vk
from keyboards.visibilityKeyboard import get_hide_keyboard, get_show_keyboard

router = Router()
round = 0

async def handle_start_round(user_id: int, message_or_callback, is_callback: bool = True):
    if user_id not in st.USER_ROOMS:
        text = "Вы не в комнате!"
        if is_callback:
            await message_or_callback.answer(text, show_alert=True)
        else:
            await message_or_callback.answer(text)
        return

    room_code = st.USER_ROOMS[user_id]
    room = st.ACTIVE_ROOMS[room_code]

    if room['host_id'] != user_id:
        text = "Только хост может начать раунд!"
        if is_callback:
            await message_or_callback.answer(text, show_alert=True)
        else:
            await message_or_callback.answer(text)
        return

    if len(room['players']) < st.MIN_PLAYERS:
        text = "❌ Игроков не хватает!"
        if is_callback:
            await message_or_callback.message.answer(text)
            await message_or_callback.answer()
        else:
            await message_or_callback.answer(text)
        return

    room['round'] += 1
    room['status'] = 'playing'
    result_users = gl.game_round(room['players'])

    for player_id, data in result_users.items():
        caption = f"Раунд: {room['round']}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль."
        if data['role'] == 'Spy':
            await message_or_callback.bot.send_photo(
                chat_id=player_id,
                photo=FSInputFile(st.DEFAULT_CARD_PATH),
                caption=caption,
                reply_markup=get_show_keyboard("Spy", None)
            )
        else:
            await message_or_callback.bot.send_photo(
                chat_id=player_id,
                photo=FSInputFile(st.DEFAULT_CARD_PATH),
                caption=caption,
                reply_markup=get_show_keyboard("NoSpy", data['card'])
            )

    if is_callback:
        await message_or_callback.answer()

@router.message(Command('play'))
async def lets_play(message: types.Message):
    await message.answer('Начните игру!⬇️', reply_markup=kb.main)

@router.callback_query(F.data == 'start_round')
async def start_round_callback(callback: types.CallbackQuery):
    await handle_start_round(callback.from_user.id, callback, is_callback=True)

@router.message(Command("start_round"))
async def start_round_command(message: types.Message):
    await handle_start_round(message.from_user.id, message, is_callback=False)


@router.callback_query(F.data.startswith('hide_card:'))
async def hide_card(callback: types.CallbackQuery):
    card_name = callback.data.split(':')[2]
    role = callback.data.split(':')[1]
    room_code = st.USER_ROOMS.get(callback.from_user.id)
    if not room_code or room_code not in st.ACTIVE_ROOMS:
        return
    room = st.ACTIVE_ROOMS[room_code]
    current_round = room['round']
    await callback.bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(st.DEFAULT_CARD_PATH),
            caption=f"Раунд: {current_round}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль."
        ),
        reply_markup=get_show_keyboard(role, card_name)
    )
    await callback.answer()

@router.callback_query(F.data.startswith('show_card:'))
async def show_card(callback: types.CallbackQuery):
    card_name = callback.data.split(':')[2]
    role = callback.data.split(':')[1]

    room_code = st.USER_ROOMS.get(callback.from_user.id)
    if not room_code or room_code not in st.ACTIVE_ROOMS:
        return
    room = st.ACTIVE_ROOMS[room_code]
    current_round = room['round']

    if role == "Spy":
        await callback.bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(
                media=FSInputFile(st.DEFAULT_CARD_PATH),
                caption=f'Раунд: {current_round}\n🥷🏻 Вы шпион!\n🤫 Не выдавайте себя и постарайтесь угадать, какая карта у других!'
            ),
            reply_markup=get_hide_keyboard(role, card_name)
        )
    else:
        original_photo_path = os.path.join(st.IMAGE_DIR, f"{card_name}.webp")
        photo = FSInputFile(original_photo_path)
        caption = f'Раунд: {current_round}\nВаша карта: {card_name}!\nУдачи в поиске шпиона!'
        await callback.bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=photo, caption=caption),
            reply_markup=get_hide_keyboard(role, card_name)
        )
    
    await callback.answer()