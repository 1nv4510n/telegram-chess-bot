import asyncio
from aiogram import Bot, Router, F, html
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove
from aiogram.filters import Command, Text
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.filters.search_filter import UserPlayingFilter
from bot.filters.chess_filter import ValidTurnFilter

from bot.states import ChessStates
from bot.keyboards.kb_default import make_menu_keyboard
from bot.keyboards.kb_chess import *
from bot.db.requests import update_user_data, log_game

from bot.chess import Game, Player
from bot.chess.enums import ChessStatus
from bot.utils import make_game_dict, change_user_ratings

router = Router()

@router.message(UserPlayingFilter(playing=True), Text('Resign'))
@router.message(UserPlayingFilter(playing=True), Command('resign'))
async def resign_game_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession) -> None:
    current_data = await state.get_data()
    current_player: Player = current_data['player']
    current_player.status = ChessStatus.LOSE
    current_name = message.from_user.first_name
     
    enemy_id = current_data['enemy_id']
    enemy_chat = await bot.get_chat(enemy_id)
    enemy_name = enemy_chat.first_name
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    enemy_data = await fsm_storage.get_data(bot, enemy_key)
    enemy_player: Player = enemy_data['player']
    enemy_player.status = ChessStatus.WIN

    ratings = await change_user_ratings(session, current_player, enemy_player)
    await log_game(
        session,
        await make_game_dict(current_player.game_id, enemy_name, enemy_player.rating, current_player.status.value),
        message.from_user.id
    )
    await log_game(
        session,
        await make_game_dict(enemy_player.game_id, current_name, current_player.rating, enemy_player.status.value),
        enemy_id
    )
    
    await state.clear()
    await fsm_storage.set_state(bot, enemy_key, None)
    await fsm_storage.set_data(bot, enemy_key, {})
    
    resign_text = "{text}\n\n<b>Winner: {enemy_name}!</b>\n\nYour rating: <b>{new_rating} ({total_earn})</b>"
    
    await message.answer(resign_text.format(
        text='You have successfully surrendered.',
        enemy_name=enemy_name,
        new_rating=ratings[0][1],
        total_earn=ratings[0][0] if ratings[0][0] < 0 else f'+{ratings[0][0]}'
        ), 
        reply_markup=make_menu_keyboard()
    )
    
    await bot.send_message(enemy_id, resign_text.format(
        text='The game is over, the enemy has surrendered.',
        enemy_name=enemy_name,
        new_rating=ratings[1][1],
        total_earn=ratings[1][0] if ratings[1][0] < 0 else f'+{ratings[1][0]}'
        ), 
        reply_markup=make_menu_keyboard()
    )
    
    for id in (message.from_user.id, enemy_id):
        await update_user_data(session, id, searching=False, playing=False, game_id=None)
        
@router.message(UserPlayingFilter(playing=True), ValidTurnFilter(), Text('Change piece'))
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
async def select_target_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession) -> None:
    current_data = await state.get_data()
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    enemy_id: int = current_data['enemy_id']
    if message.text not in current_data['targets']:
        await message.answer('<b>INVALID TARGET</b>\nPlease, select a target from the buttons.')
        return

    piece = current_data['piece']
    target = message.text
    
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    enemy_data = await fsm_storage.get_data(bot, enemy_key)
    enemy_player: Player = enemy_data['player']
    
    current_board = await current_game.move_piece(piece, target)
    enemy_board = await current_game.get_board_image(enemy_player)
    
    await message.answer_photo(photo=BufferedInputFile(current_board, 'board.jpg'))
    await asyncio.sleep(0.5)
    await bot.send_photo(enemy_id, photo=BufferedInputFile(enemy_board, 'board.jpg'))
    
    if current_game.is_gameover == False:
        await message.answer(
            f"""Your move: <b>{piece}-{target}</b>\n\n{html.italic("Waiting for opponent's move...")}""", 
            reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(ChessStates.waiting_move)

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
    else:
        await message.answer(f'Your move: <b>{piece}-{target}</b>')
        await bot.send_message(enemy_id, f"Oponent's move: {piece}-{target}")
        await update_user_data(session, message.from_user.id, searching=False, playing=False, game_id=None)
        await update_user_data(session, enemy_id, searching=False, playing=False, game_id=None)
        ratings = await change_user_ratings(session, current_player, enemy_player)
                
        end_message = "<b>THE GAME IS OVER\n\n{status}!</b>\n\nGAME RESULT: <b>{game_status}</b>\n\nYOUR RATING: <b>{new_rating} ({total_earn})</b>"
        await message.answer(
            text=end_message.format(
                status=current_player.status.value if current_player.status == ChessStatus.DRAW else f'YOU {current_player.status.value}',
                game_status=current_game.end_game_status.value,
                new_rating=ratings[0][1],
                total_earn=ratings[0][0] if ratings[0][0] < 0 else f'+{ratings[0][0]}'
                ),
                reply_markup=make_menu_keyboard()
            )
        await bot.send_message(
            enemy_id,
            text=end_message.format(
                status=enemy_player.status.value if enemy_player.status == ChessStatus.DRAW else f'YOU {enemy_player.status.value}',
                game_status=current_game.end_game_status.value,
                new_rating=ratings[1][1],
                total_earn=ratings[1][0] if ratings[1][0] < 0 else f'+{ratings[1][0]}'
            ),
            reply_markup=make_menu_keyboard()
        )
        current_name = message.from_user.first_name
        enemy_chat = await bot.get_chat(enemy_id)
        enemy_name = enemy_chat.first_name
        
        await log_game(
            session,
            await make_game_dict(current_player.game_id, enemy_name, enemy_player.rating, current_player.status.value),
            current_player.id
        )
        await log_game(
            session,
            await make_game_dict(enemy_player.game_id, current_name, current_player.rating, enemy_player.status.value),
            enemy_player.id
        )
        
        await state.clear()
        await fsm_storage.set_state(bot, enemy_key, None)
        await fsm_storage.set_data(bot, enemy_key, {})
            
        
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
async def check_escape_move_handler(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession) -> None:
    current_data = await state.get_data()
    if message.text not in current_data['escape_moves']:
        await message.answer('<b>INVALID TARGET</b>\nPlease, select an target from the buttons.')
        return
    current_game: Game = current_data['game']
    current_player: Player = current_data['player']
    enemy_id: int = current_data['enemy_id']
    enemy_key = StorageKey(bot.id, enemy_id, enemy_id)
    enemy_data = await fsm_storage.get_data(bot, enemy_key)
    enemy_player: Player = enemy_data['player']

    move = message.text
    
    select_cell = move.split('-')[0]
    target_cell = move.split('-')[1]
    
    current_game.current_turn.status = None
    
    current_board = await current_game.move_piece(select_cell, target_cell)
    enemy_board = await current_game.get_board_image(enemy_player)
    await message.answer_photo(photo=BufferedInputFile(current_board, 'board.jpg'))    
    await bot.send_photo(enemy_id, BufferedInputFile(enemy_board, 'board.jpg'), disable_notification=False)
    
    if current_game.is_gameover == False:
        await message.answer(
            f"""Your move: <b>{move}</b>\n\n{html.italic("Waiting for opponent's move...")}""", 
            reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(ChessStates.waiting_move)
        await state.update_data(escape_moves={})
        await asyncio.sleep(0.5)
        
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
    else:
        await message.answer(f'Your move: <b>{move}</b>')
        await bot.send_message(enemy_id, f"Oponent's move: {move}")   
        await update_user_data(session, message.from_user.id, searching=False, playing=False, game_id=None)
        await update_user_data(session, enemy_id, searching=False, playing=False, game_id=None)
        ratings = await change_user_ratings(session, current_player, enemy_player)
        
        end_message = "<b>THE GAME IS OVER\n\n{status}!</b>\n\nGAME RESULT: <b>{game_status}</b>\n\nYOUR RATING: <b>{new_rating} ({total_earn})</b>"
        await message.answer(
            text=end_message.format(
                status=current_player.status.value if current_player.status == ChessStatus.DRAW else f'YOU {current_player.status.value}',
                game_status=current_game.end_game_status.value,
                new_rating=ratings[0][1],
                total_earn=ratings[0][0] if ratings[0][0] < 0 else f'+{ratings[0][0]}'
                ),
            reply_markup=make_menu_keyboard()
            )
        await bot.send_message(
            enemy_id,
            text=end_message.format(
                status=enemy_player.status.value if enemy_player.status == ChessStatus.DRAW else f'YOU {enemy_player.status.value}',
                game_status=current_game.end_game_status.value,
                new_rating=ratings[1][1],
                total_earn=ratings[1][0] if ratings[1][0] < 0 else f'+{ratings[1][0]}'
            ),
            reply_markup=make_menu_keyboard()
        )   

        current_name = message.from_user.first_name
        enemy_chat = await bot.get_chat(enemy_id)
        enemy_name = enemy_chat.first_name
        
        await log_game(
            session,
            await make_game_dict(current_player.game_id, enemy_name, enemy_player.rating, current_player.status.value),
            current_player.id
        )
        await log_game(
            session,
            await make_game_dict(enemy_player.game_id, current_name, current_player.rating, enemy_player.status.value),
            enemy_player.id
        )
        
        await state.clear()
        await fsm_storage.set_state(bot, enemy_key, None)
        await fsm_storage.set_data(bot, enemy_key, {})