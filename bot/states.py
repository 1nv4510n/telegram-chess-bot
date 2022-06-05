from aiogram.dispatcher.fsm.state import State, StatesGroup

class ChessStates(StatesGroup):
    searching = State()
    select_icon = State()
    select_piece = State()
    select_target = State()
    waiting_move = State()