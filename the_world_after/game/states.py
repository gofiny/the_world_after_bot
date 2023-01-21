from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    ask_username = State()
