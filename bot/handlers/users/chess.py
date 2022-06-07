import asyncio
from aiogram import Bot, Router, F, html
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.filters.search_filter import UserPlayingFilter

from bot.states import ChessStates
from bot.keyboards.kb_default import make_menu_keyboard
from bot.keyboards.kb_chess import *
from bot.db.requests import update_user_data, log_game

from bot.chess import Game, Player
from bot.chess.draw import draw_board

router = Router()

@router.message(UserPlayingFilter(playing=True), F.text == 'Resign')
@router.message(UserPlayingFilter(playing=True), commands=['resign'])
async def resign_game_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession) -> None:
    current_data = await state.get_data()
    enemy_id = current_data['enemy_id']
    enemy_chat = await bot.get_chat(enemy_id)
    enemy_name = enemy_chat.first_name
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    
    await state.clear()
    await fsm_storage.set_state(bot, enemy_key, None)
    await fsm_storage.set_data(bot, enemy_key, {})
    
    await message.answer(f'You have successfully surrendered.\n\n<b>Winner: {enemy_name}</b>', reply_markup=make_menu_keyboard())
    
    await bot.send_message(enemy_id, f'The game is over, the enemy has surrendered.\n\n<b>Winner: {enemy_name}</b>', reply_markup=make_menu_keyboard())
    
    for id in (message.from_user.id, enemy_id):
        await update_user_data(session, id, searching=False, playing=False, game_id=None)

@router.message(UserPlayingFilter(playing=True), F.text == 'Change piece')
async def change_piece_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    pieces = await current_game.get_active_pieces(current_player)
    
    await message.answer('Select your piece.', reply_markup=make_pieces_keyboard(pieces), disable_notification=True)
    await state.set_state(ChessStates.select_icon)
    
@router.message(ChessStates.select_icon)
async def select_icon_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    icon = message.text
    select_pieces = await current_game.get_select_pieces(current_player, icon)
    
    await message.answer('Select your piece.', reply_markup=make_select_keyboard(select_pieces), disable_notification=True)
    await state.set_state(ChessStates.select_piece)
    
@router.message(ChessStates.select_piece)
async def select_piece_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    piece = message.text
    targets = await current_game.get_targets(current_player, piece)
    
    await message.answer('Select target.', reply_markup=make_target_keyboard(targets), disable_notification=True)
    await state.set_state(ChessStates.select_target)
    await state.update_data(piece=piece)
    
@router.message(ChessStates.select_target)
async def select_target_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    enemy_id: int = current_data['enemy_id']
    
    piece = current_data['piece']
    target = message.text
    
    current_board = await current_game.move_piece(current_player, piece, target)
    
    await message.answer_photo(photo=BufferedInputFile(current_board, 'board.jpg'))
    await message.answer(
        f"""Your move: <b>{piece}-{target}</b>\n\n{html.italic("Waiting for opponent's move...")}""", 
        reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(ChessStates.waiting_move)
    await asyncio.sleep(0.5)
    
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    enemy_data = await fsm_storage.get_data(bot, enemy_key)
    enemy_player = enemy_data['player']
    enemy_board = await current_game.get_board_image(enemy_player)
    enemy_pieces = await current_game.get_active_pieces(enemy_player)
    
    await bot.send_photo(enemy_id, photo=BufferedInputFile(enemy_board, 'board.jpg'))
    await bot.send_message(
        enemy_id, 
        f"Opponent's move: <b>{piece}-{target}</b>\n\n<b>Now it's your turn.</b>",
        reply_markup=make_pieces_keyboard(enemy_pieces)
        )
    await fsm_storage.set_state(bot, enemy_key, ChessStates.select_icon)