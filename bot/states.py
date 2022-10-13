from aiogram.fsm.state import State, StatesGroup

class ChessStates(StatesGroup):
    searching = State()
    select_icon = State()
    select_piece = State()
    select_target = State()
    under_check = State()
    check_escape_move = State()
    waiting_move = State()