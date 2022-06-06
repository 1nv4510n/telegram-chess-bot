from aiogram import Bot, Router, F
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.filters.search_filter import UserPlayingFilter

from bot.states import ChessStates
from bot.keyboards.kb_default import make_menu_keyboard
from bot.db.requests import update_user_data, log_game

router = Router()

@router.message(UserPlayingFilter(playing=True), F.text == 'Resign')
@router.message(UserPlayingFilter(playing=True), commands=['resign'])
async def resign_game(message: Message, bot: Bot, fsm_storage: MemoryStorage, state: FSMContext, session: AsyncSession) -> None:
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