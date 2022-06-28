import asyncio
from aiogram import Bot, Router, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from sqlalchemy.ext.asyncio.session import AsyncSession
import random
from uuid import uuid4

from bot.db.requests import update_user_data, get_searching_users, get_user_rating
from bot.keyboards.kb_default import make_searching_keyboard
from bot.keyboards.kb_chess import make_icons_keyboard
from bot.utils.logging import log
from bot.states import ChessStates

from bot.chess.enums import Colors, PieceIcons
from bot.chess.player import Player
from bot.chess.game import Game

router = Router()

@router.callback_query(ChessStates.searching, text='stop_search')
async def stop_search(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await update_user_data(session, call.from_user.id, searching=False, playing=False)
    await state.clear()
    await call.message.edit_text('<b>Game search stopped.</b>')

@router.message(F.text == 'New game')
@router.message(commands=['new_game'])
async def new_game(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession):
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("Can't start new game.\n<b>You are already playing/searching!</b>")
        return
    msg = await message.answer("<b>Searching game...</b>", reply_markup=make_searching_keyboard())
    if message.from_user.username:
        log.info(f'User @{message.from_user.username} ({message.from_user.first_name}) started search')
    else:
        log.info(f'User {message.from_user.first_name} started search')
    
    await asyncio.sleep(30 / random.randint(10, 100))
    await update_user_data(session, message.chat.id, searching=True, playing=False, name=message.from_user.first_name)
    await state.set_state(ChessStates.searching)
    
    searching_players = [user.telegram_id for user in await get_searching_users(session)]
    searching_players.remove(message.from_user.id)
    
    if len(searching_players) == 1:
        game_id = str(uuid4())
        random_id = random.choice(searching_players)
    
        player1 = Player(
            id=random_id,
            rating=await get_user_rating(session, random_id),
            game_id=game_id,
            color=random.choice((Colors.WHITE, Colors.BLACK)),
            status=None
        )
        
        player2 = Player(
            id=message.from_user.id,
            rating=await get_user_rating(session, message.from_user.id),
            game_id=game_id,
            color=Colors.WHITE if player1.color == Colors.BLACK else Colors.BLACK,
            status=None
        )
        await update_user_data(session, player1.id, searching=False, playing=True, game_id=game_id)
        await update_user_data(session, player2.id, searching=False, playing=True, game_id=game_id)
        
        player1_key = StorageKey(bot.id, player1.id, player1.id)
        player1_state = ChessStates.select_icon if player1.color == Colors.WHITE else ChessStates.waiting_move
        player2_state = ChessStates.select_icon if player2.color == Colors.WHITE else ChessStates.waiting_move
        await fsm_storage.set_state(bot, player1_key, player1_state)
        await state.set_state(player2_state)
        
        await msg.delete()
        game = Game(
            game_id=game_id,
            player1=player1,
            player2=player2
        )

        await fsm_storage.set_data(bot, player1_key, 
            data={
                'game' : game,
                'player' : player1,
                'enemy_id' : player2.id
            }
        )

        await state.set_data(
            data={
                'game' : game,
                'player' : player2,
                'enemy_id' : player1.id
            }
        )
        
        game_found_text = "<b>Game has been found!</b>\n\nYour opponent: <b>{name} ({rating})</b>\n\nYour Color: <b>{color}</b>"
        
        player1_chat = await bot.get_chat(player1.id)
        player1_name = player1_chat.first_name
        player1_board = await game.get_board_image(player1)
        
        player2_name = message.from_user.first_name
        player2_board = await game.get_board_image(player2)
        
        icons = [PieceIcons.KNIGHT, PieceIcons.PAWN]
        await state.update_data({'icons' : [icon.value for icon in icons]})
        await fsm_storage.update_data(bot, player1_key, {'icons' : [icon.value for icon in icons]})
        
        await bot.send_photo(player1.id, BufferedInputFile(file=player1_board, filename='board.jpg'))
        await asyncio.sleep(0.3)
        await bot.send_message(player1.id, 
                               game_found_text.format(name=player2_name, rating=round(player2.rating), color=player1.color.name),
                               reply_markup=make_icons_keyboard(icons))
        
        await message.answer_photo(photo=BufferedInputFile(file=player2_board, filename='board.jpg'))
        await asyncio.sleep(0.3)
        await message.answer(game_found_text.format(name=player1_name, rating=round(player1.rating), color=player2.color.name),
                               reply_markup=make_icons_keyboard(icons))