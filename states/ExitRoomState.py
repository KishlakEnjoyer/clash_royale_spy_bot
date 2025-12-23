from aiogram.fsm.state import State, StatesGroup

class ExitRoom(StatesGroup):
    wait_for_exit = State()