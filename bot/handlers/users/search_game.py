import asyncio
from aiogram import Bot, Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio.session import AsyncSession
import random
from uuid import uuid4

from bot.db.requests import update_user_data, get_searching_users
from bot.keyboards.kb_default import make_searching_keyboard, make_menu_keyboard
from bot.states import ChessStates

router = Router()

@router.message(F.text == 'New game')
async def new_game(message: Message, bot: Bot, state: FSMContext, session: AsyncSession):
    searching_players = [user.telegram_id for user in await get_searching_users(session)]
    
    await update_user_data(session, message.chat.id, searching=True, playing=False)
    await state.set_state(ChessStates.searching)

    await message.answer(
        f"<b>Searching game...</b>\n\nPlayers looking for a game: <b>{len(searching_players) + 1}</b>",
        reply_markup=make_searching_keyboard()
    )
    await asyncio.sleep(1)
    
    if len(searching_players) >= 1:
        opponent_id = random.choice(searching_players)
        
        game_id = uuid4()
        
        await update_user_data(session, message.chat.id, searching=False, playing=True, game_id=game_id)
        await update_user_data(session, opponent_id, searching=False, playing=True, game_id=game_id)
        
        
@router.message(ChessStates.searching, F.text == 'Stop search')
async def stop_search(message: Message, state: FSMContext, session: AsyncSession):
    await update_user_data(session, message.chat.id, searching=False, playing=False)
    await state.clear()
    
    await message.answer('<b>Game search stopped.</b>', reply_markup=make_menu_keyboard())