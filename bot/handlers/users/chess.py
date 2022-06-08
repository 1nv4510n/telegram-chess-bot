import asyncio
from aiogram import Bot, Router, F, html
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio.session import AsyncSession
from bot.chess.enums import ChessStatus

from bot.filters.search_filter import UserPlayingFilter
from bot.filters.chess_filter import ValidTurnFilter

from bot.states import ChessStates
from bot.keyboards.kb_default import make_menu_keyboard
from bot.keyboards.kb_chess import *
from bot.db.requests import update_user_data, log_game

from bot.chess import Game, Player

router = Router()

####### TEST #######
@router.message(ValidTurnFilter(), F.text == 'is under check')
async def under_check_test(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    is_check = current_game.board.king_escape_moves(current_player.color)
    
    if is_check:
        await message.answer('CHECK')
        
####################

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

@router.message(UserPlayingFilter(playing=True), ValidTurnFilter(), F.text == 'Change piece')
async def change_piece_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    
    icons = current_data['icons']
    
    if current_game.current_turn.status == ChessStatus.CHECK:
        await message.answer('Choose an icon to escape the check', reply_markup=make_icons_keyboard(icons, string_mode=True), disable_notification=True)
        await state.set_state(ChessStates.under_check)
    else:
        await message.answer('Select your piece.', reply_markup=make_icons_keyboard(icons, string_mode=True), disable_notification=True)
        await state.set_state(ChessStates.select_icon)
    
@router.message(ValidTurnFilter(), ChessStates.select_icon)
async def select_icon_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']

    if message.text not in current_data['icons']:
        await message.answer('<b>INVALID PIECE</b>\nPlease, select an icon from the buttons.')
        return
    icon = message.text
    
    select_pieces = await current_game.get_select_pieces(icon)
    await state.update_data(pieces=select_pieces)
    
    await message.answer('Select your piece.', reply_markup=make_select_keyboard(select_pieces), disable_notification=True)
    await state.set_state(ChessStates.select_piece)
    
@router.message(ValidTurnFilter(), ChessStates.select_piece)
async def select_piece_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    if message.text not in current_data['pieces']:
        await message.answer('<b>INVALID PIECE</b>\nPlease, select a piece from the buttons.')
        return
    
    piece = message.text
    targets = await current_game.get_targets(piece)
    await state.update_data(targets=targets)
    
    await message.answer('Select target.', reply_markup=make_target_keyboard(targets), disable_notification=True)
    await state.set_state(ChessStates.select_target)
    await state.update_data(piece=piece)
    
@router.message(ValidTurnFilter(), ChessStates.select_target)
async def select_target_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    enemy_id: int = current_data['enemy_id']
    if message.text not in current_data['targets']:
        await message.answer('<b>INVALID TARGET</b>\nPlease, select a target from the buttons.')
        return

    piece = current_data['piece']
    target = message.text
    
    current_board = await current_game.move_piece(piece, target)
    
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
    await bot.send_photo(enemy_id, photo=BufferedInputFile(enemy_board, 'board.jpg'))
    
    if not current_game.current_turn.status == ChessStatus.CHECK:
        enemy_icons = await current_game.get_active_pieces()

        await bot.send_message(
            enemy_id, 
            f"Opponent's move: <b>{piece}-{target}</b>\n\n<b>Now it's your turn.</b>",
            reply_markup=make_icons_keyboard(enemy_icons)
            )
        await fsm_storage.set_state(bot, enemy_key, ChessStates.select_icon)
        await fsm_storage.update_data(bot, enemy_key, {'icons' : [icon.value for icon in enemy_icons]})
    else:
        enemy_icons = await current_game.get_check_icons()
        await bot.send_message(
            enemy_id, 
            f"Opponent's move: <b>{piece}-{target}</b>\n\n<b>!!! CHECK !!!</b>",
            reply_markup=make_icons_keyboard(enemy_icons)
            )
        await fsm_storage.set_state(bot, enemy_key, ChessStates.under_check)
        await fsm_storage.update_data(bot, enemy_key, {'icons': [icon.value for icon in enemy_icons]})
        
@router.message(ValidTurnFilter(), ChessStates.under_check)
async def under_check_handler(message: Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    if message.text not in current_data['icons']:
        await message.answer('<b>INVALID PIECE</b>\nPlease, select an icon from the buttons.')
        return
    current_game: Game = current_data['game']
    icon = message.text
    escape_moves = await current_game.get_check_escape_moves(icon)
    await state.update_data(escape_moves=escape_moves)
    
    await message.answer('Chose a move to escape the check', reply_markup=make_select_keyboard(escape_moves))
    await state.set_state(ChessStates.check_escape_move)
    
@router.message(ValidTurnFilter(), ChessStates.check_escape_move)
async def check_escape_move_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext) -> None:
    current_data = await state.get_data()
    if message.text not in current_data['escape_moves']:
        await message.answer('<b>INVALID TARGET</b>\nPlease, select an target from the buttons.')
        return
    current_game: Game = current_data['game']
    enemy_id: int = current_data['enemy_id']
    move = message.text
    
    select_cell = move.split('-')[0]
    target_cell = move.split('-')[1]
    
    current_game.current_turn.status = None
    current_board = await current_game.move_piece(select_cell, target_cell)
    await message.answer_photo(photo=BufferedInputFile(current_board, 'board.jpg'))
    await message.answer(
        f"""Your move: <b>{move}</b>\n\n{html.italic("Waiting for opponent's move...")}""", 
        reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(ChessStates.waiting_move)
    await state.update_data(escape_moves={})
    await asyncio.sleep(0.5)
    
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    enemy_data = await fsm_storage.get_data(bot, enemy_key)
    enemy_player = enemy_data['player']
    enemy_board = await current_game.get_board_image(enemy_player)
    
    await bot.send_photo(enemy_id, BufferedInputFile(enemy_board, 'board.jpg'), disable_notification=False)
    
    if not current_game.current_turn.status == ChessStatus.CHECK:
        enemy_icons = await current_game.get_active_pieces()

        await bot.send_message(
            enemy_id, 
            f"Opponent's move: <b>{move}</b>\n\n<b>Now it's your turn.</b>",
            reply_markup=make_icons_keyboard(enemy_icons)
            )
        await fsm_storage.set_state(bot, enemy_key, ChessStates.select_icon)
        await fsm_storage.update_data(bot, enemy_key, {'icons' : [icon.value for icon in enemy_icons]})
    else:
        enemy_icons = await current_game.get_check_icons()
        await bot.send_message(
            enemy_id, 
            f"Opponent's move: <b>{move}</b>\n\n<b>!!! CHECK !!!</b>",
            reply_markup=make_icons_keyboard(enemy_icons)
            )
        await fsm_storage.set_state(bot, enemy_key, ChessStates.under_check)
        await fsm_storage.update_data(bot, enemy_key, {'icons': [icon.value for icon in enemy_icons]})