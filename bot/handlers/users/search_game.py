import asyncio
from aiogram import Bot, Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
import random
from uuid import uuid4

from bot.db.requests import update_user_data, get_searching_users
from bot.keyboards.kb_default import make_searching_keyboard, make_menu_keyboard
from bot.keyboards.kb_chess import make_pieces_keyboard
from bot.states import ChessStates

from bot.chess.enums import Colors
from bot.chess.player import Player
from bot.chess.game import Game

white_board_id = 'AgACAgIAAxkDAAIFBWKeYNoX9DgRKFpkAe0m7p7RJrKfAALzvTEbPZzxSG7cOa7BI5ggAQADAgADbQADJAQ'
black_board_id = 'AgACAgIAAxkDAAIFB2KeYNv0XC-bQrsgtavJVqro9srWAALauzEbQUPwSPa9z_dKH3wLAQADAgADbQADJAQ'

router = Router()

@router.message(ChessStates.searching, F.text == 'Stop search')
@router.message(ChessStates.searching, commands=['stop'])
async def stop_search(message: Message, state: FSMContext, session: AsyncSession):
    await update_user_data(session, message.chat.id, searching=False, playing=False)
    await state.clear()
    
    await message.answer('<b>Game search stopped.</b>', reply_markup=make_menu_keyboard())
    
@router.message(F.text == 'New game')
@router.message(commands=['new_game'])
async def new_game(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("Can't start new game.\n<b>You are already playing!</b>")
        return
    
    searching_players = [user.telegram_id for user in await get_searching_users(session)]
    
    await update_user_data(session, message.chat.id, searching=True, playing=False)
    await state.set_state(ChessStates.searching)
    await message.answer(
        f"<b>Searching game...</b>\n\nPlayers looking for a game: <b>{len(searching_players) + 1}</b>",
        reply_markup=make_searching_keyboard()
    )
    await asyncio.sleep(1)

    if len(searching_players) >= 1:
        game_id = str(uuid4())
        
        player1 = Player(
            id=random.choice(searching_players),
            game_id=game_id,
            color=random.choice((Colors.WHITE, Colors.BLACK))
        )
        player1_key = StorageKey(bot.id, player1.id, player1.id)
        player1_state = ChessStates.select_icon if player1.color == Colors.WHITE else ChessStates.waiting_move
        
        player2 = Player(
            id=message.from_user.id,
            game_id=game_id,
            color=Colors.WHITE if player1.color == Colors.BLACK else Colors.BLACK
        )
        player2_state = ChessStates.select_icon if player2.color == Colors.WHITE else ChessStates.waiting_move
        
        game = Game(
            game_id=game_id,
            player1=player1,
            player2=player2,
        )
        
        #player1
        await update_user_data(session, player1.id, searching=False, playing=True, game_id=game_id)
        await fsm_storage.set_state(bot, player1_key, player1_state)
        await fsm_storage.set_data(bot, player1_key, 
            data={
                'game' : game,
                'player' : player1,
                'enemy_id' : player2.id
            }
        )
         
        #player2
        await update_user_data(session, player2.id, searching=False, playing=True, game_id=game_id)
        await state.set_state(player2_state)
        await state.set_data(
            data={
                'game' : game,
                'player' : player2,
                'enemy_id' : player1.id
            }
        )
        
        game_found_text = "<b>Game has been found!</b>\n\nYour opponent: <b>{name}</b>\n\nYour Color: <b>{color}</b>"
        
        player1_chat = await bot.get_chat(player1.id)
        player1_name = player1_chat.first_name
        board1 = white_board_id if player1.color == Colors.WHITE else black_board_id
        
        player2_name = message.from_user.first_name
        board2 = white_board_id if player2.color == Colors.WHITE else black_board_id
        
        pieces = await game.get_active_pieces(player1)
        
        await bot.send_photo(player1.id, board1)
        await asyncio.sleep(0.5)
        await bot.send_message(player1.id, 
                               game_found_text.format(name=player2_name, color=player1.color.name),
                               reply_markup=make_pieces_keyboard(pieces))
        
        await message.answer_photo(board2)
        await asyncio.sleep(0.5)
        await message.answer(game_found_text.format(name=player1_name, color=player2.color.name),
                               reply_markup=make_pieces_keyboard(pieces))