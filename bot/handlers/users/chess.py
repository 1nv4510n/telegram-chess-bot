from aiogram import Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.states import ChessStates
from bot.db.requests import is_user_exists

router = Router()

@router.message(F.text == 'New game')
async def new_game(message: Message, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    # if current_state is None:
    #     message.answer("Can't start new game. \nFinish the current game.")
    #     return 
