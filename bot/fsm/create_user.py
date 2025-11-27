from aiogram.fsm.state import State, StatesGroup

class CreateUser(StatesGroup):
    name = State()
    suggestion = State()