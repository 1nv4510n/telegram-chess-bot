from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext

from bot.states import ChessStates

class ValidTurnFilter(BaseFilter):
    def __init__(self) -> None:
        super().__init__()
    
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        if current_state is None or current_state == ChessStates.searching.state:
            return False
        
        current_data = await state.get_data()
        current_game = current_data['game']
        current_player = current_data['player']
        return current_game.current_turn == current_player
