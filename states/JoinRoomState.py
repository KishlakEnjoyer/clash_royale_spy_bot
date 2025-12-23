from aiogram.fsm.state import State, StatesGroup

class JoinRoom(StatesGroup):
    waiting_for_code = State()