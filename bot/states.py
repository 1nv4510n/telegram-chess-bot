from aiogram.dispatcher.fsm.state import State, StatesGroup

class Poll(StatesGroup):
    name = State()
    age = State()
    phone = State()
    city = State()