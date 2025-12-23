from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import game_logic as gl
import storage as st
import keyboards.playMenuKeyboard as kb
import keyboards.mainKeyboard as mainkb
import states.JoinRoomState as JoinRoom
import states.ExitRoomState as ExitRoom


router = Router()

@router.callback_query(F.data == 'create_room')
async def create_room_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in st.USER_ROOMS:
        await callback.answer("Вы уже в комнате!", show_alert=True)
        return

    code = gl.generate_room_code(user_id)
    await callback.message.edit_text(
        f"✅ Комната создана!\nКод: <b>{code}</b>\nПоделитесь кодом с друзьями!",
        reply_markup=kb.host_menu,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'join_room')
async def join_room_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите код комнаты, к которой хотите присоединиться:", reply_markup=mainkb.back)
    await state.set_state(JoinRoom.JoinRoom.waiting_for_code)
    await callback.answer()

@router.message(JoinRoom.JoinRoom.waiting_for_code)
async def process_room_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    room_code = message.text.strip()

    if user_id in st.USER_ROOMS:
        await message.answer("Вы уже в комнате!", show_alert=True)
        await state.clear()
        return

    if room_code not in st.ACTIVE_ROOMS:
        await message.answer("Комната не найдена.")
        await message.answer("Вернуться в меню:", reply_markup=mainkb.main)
        await state.clear()
        return

    room = st.ACTIVE_ROOMS[room_code]

    if room['status'] != 'waiting':
        await message.answer(f"В комнате {room_code} пока идет игра!\nВовзращайтесь позже!")
        return 
    room['players'].append(user_id)
    st.USER_ROOMS[user_id] = room_code

    await message.answer(
    f"✅ Вы присоединились к комнате {room_code}!\n⏳ Ожидайте запуск раунда!",
    reply_markup=kb.player_menu
    )
    await message.bot.send_message(chat_id=room['host_id'], text=f'Присоединился игрок {message.from_user.first_name}!\nВсего игроков: {len(room['players'])}')

    await state.clear()

@router.callback_query(F.data == 'leave_room')
async def leave_room_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in st.USER_ROOMS:
        await callback.answer("Вы не в комнате.", show_alert=True)
        return

    room_code = st.USER_ROOMS[user_id]
    room = st.ACTIVE_ROOMS[room_code]
    room['players'].remove(user_id)

    if user_id == room['host_id']:
        if room['players']:
            await callback.message.edit_text(
                f"Вы вышли из комнаты {room_code}. Права хоста переданы.")
        else:
            del st.ACTIVE_ROOMS[room_code]
            await callback.message.edit_text(
                f"Комната {room_code} закрыта (вы были последним).")
    else:
        await callback.message.edit_text(
            f"Вы вышли из комнаты {room_code}.")
        await callback.message.bot.send_message(chat_id=room['host_id'], text=f'Игрок {callback.from_user.first_name} вышел из комнаты!') 

    del st.USER_ROOMS[user_id]

    await callback.message.answer("Начните игру!⬇️", reply_markup=mainkb.main)
    await callback.answer()

@router.message(Command('leave_room'))
async def leave_room_callback(message: types.Message):
    user_id = message.from_user.id

    if user_id not in st.USER_ROOMS:
        await message.answer("Вы не в комнате.", show_alert=True)
        return

    room_code = st.USER_ROOMS[user_id]
    room = st.ACTIVE_ROOMS[room_code]
    room['players'].remove(user_id)

    if user_id == room['host_id']:
        if room['players']:
            await message.edit_text(
                f"Вы вышли из комнаты {room_code}. Права хоста переданы.")
        else:
            del st.ACTIVE_ROOMS[room_code]
            await message.edit_text(
                f"Комната {room_code} закрыта (вы были последним).")
    else:
        await message.edit_text(
            f"Вы вышли из комнаты {room_code}.")
        await message.bot.send_message(chat_id=room['host_id'], text=f'Игрок {message.from_user.first_name} вышел из комнаты!') 

    del st.USER_ROOMS[user_id]

    await message.answer("Начните игру!⬇️", reply_markup=mainkb.main)


@router.callback_query(F.data == 'back')
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    
    await state.clear()
    
    await callback.message.edit_text(
        "Выберите действие:",
        reply_markup=mainkb.main
    )
    await callback.answer()