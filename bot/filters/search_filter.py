from aiogram.types import Message
from aiogram.dispatcher.filters.base import BaseFilter
from aiogram.dispatcher.fsm.context import FSMContext

from bot.states import ChessStates

class UserSearchingFilter(BaseFilter):
    searching: bool
    
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        is_user_searching = (current_state == ChessStates.searching.state)
        
        if is_user_searching == self.searching:
            return True
        else:
            await message.answer("Please stop search: /stop")
            return False
        
class UserPlayingFilter(BaseFilter):
    playing: bool
    
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        current_state = await state.get_state()
        
        is_user_playing = ((current_state is not None) and (current_state != ChessStates.searching.state))
        
        if is_user_playing == self.playing:
            return True
        else:
            return False