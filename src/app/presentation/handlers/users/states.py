from aiogram.fsm.state import State, StatesGroup


class BirthdayStates(StatesGroup):
    waiting_for_owner = State()
    waiting_for_date = State()
    waiting_for_update_owner = State()
    waiting_for_update_date = State()
