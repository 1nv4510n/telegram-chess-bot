from typing import Dict, List
from contextlib import suppress

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.db.models import GamesHistoryEntry, PlayersEntry

async def get_game_history(session: AsyncSession, telegram_id: int) -> List[GamesHistoryEntry]:
    game_data_request = await session.execute(
        select(GamesHistoryEntry).where(GamesHistoryEntry.telegram_id == telegram_id)
    )
    return game_data_request.scalars().all()

async def is_user_exists(session: AsyncSession, telegram_id: int) -> bool:
    request = await session.execute(
        select(PlayersEntry).filter_by(telegram_id=telegram_id)
    )
    return request.scalars().first() is not None
    
async def add_user(session: AsyncSession, telegram_id: int) -> None:
    entry = PlayersEntry()
    entry.telegram_id = telegram_id
    entry.searching = False
    entry.playing = False
    session.add(entry)
    with suppress(IntegrityError):
        await session.commit()
    
async def log_game(session: AsyncSession, data: Dict, telegram_id: int) -> None:
    entry = GamesHistoryEntry()
    entry.game_id = data['game_id']
    entry.telegram_id = telegram_id
    entry.opponent_name = data['opponent_name']
    entry.color = data['color']
    entry.result = data['result']
    session.add(entry)
    with suppress(IntegrityError):
        await session.commit()