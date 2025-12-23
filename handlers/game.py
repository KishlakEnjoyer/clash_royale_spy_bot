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

@router.message(Command('play'))
async def lets_play(message: types.Message):
    await message.answer('Начните игру!⬇️', reply_markup=kb.main)

@router.message(Command('start_round'))
async def send_photo_command(message: types.Message):
    host_id = message.from_user.id
    room_code = st.USER_ROOMS[host_id]
    current_room = st.ACTIVE_ROOMS[room_code]
    current_room['round'] += 1

    if len(current_room['players']) < st.MIN_PLAYERS:
        await message.answer(text=f'❌ Игроков не хватает!')
        return
    
    current_room['status'] = 'playing'
    result_users = gl.game_round(current_room['players'])
    for key, value in result_users.items():
        
        if value['role'] == 'Spy':
            await message.bot.send_photo(
                            chat_id=key,
                            photo=FSInputFile(st.DEFAULT_CARD_PATH),
                            caption=f"Раунд: {current_room['round']}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль.",
                            reply_markup=get_show_keyboard("Spy", None)
                        )
            continue
        await message.bot.send_photo(
                        chat_id=key,
                        photo=FSInputFile(st.DEFAULT_CARD_PATH),
                        caption=f"Раунд: {current_room['round']}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль.",
                        reply_markup=get_show_keyboard("NoSpy", value['card'])
                    )

@router.callback_query(F.data == 'start_round')
async def send_photo(callback: types.CallbackQuery):
    host_id = callback.from_user.id
    room_code = st.USER_ROOMS[host_id]
    current_room = st.ACTIVE_ROOMS[room_code]
    current_room['round'] += 1

    if len(current_room['players']) < st.MIN_PLAYERS:
        await callback.message.answer(text=f'❌ Игроков не хватает!')
        await callback.answer()
        return
    
    current_room['status'] = 'playing'
    result_users = gl.game_round(current_room['players'])

    for key, value in result_users.items():
        if value['role'] == 'Spy':
            await callback.bot.send_photo(
                            chat_id=key,
                            photo=FSInputFile(st.DEFAULT_CARD_PATH),
                            caption=f"Раунд: {current_room['round']}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль.",
                            reply_markup=get_show_keyboard("Spy", None)
                        )
            continue
        await callback.bot.send_photo(
                        chat_id=key,
                        photo=FSInputFile(st.DEFAULT_CARD_PATH),
                        caption=f"Раунд: {current_room['round']}\nКарта скрыта. Нажмите «Показать», чтобы увидеть свою роль.",
                        reply_markup=get_show_keyboard("NoSpy", value['card'])
                    )
    await callback.answer()


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