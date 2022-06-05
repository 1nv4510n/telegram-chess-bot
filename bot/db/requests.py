from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import GamesHistoryEntry

async def get_game_history(session: AsyncSession, telegram_id: int) -> List[GamesHistoryEntry]:
    game_data_request = await session.execute(
        select(GamesHistoryEntry).where(GamesHistoryEntry.telegram_id == telegram_id)
    )
    return game_data_request.scalars().all()

async def log_game(session: AsyncSession, data: Dict, telegram_id: int) -> None:
    entry = GamesHistoryEntry()
    entry.game_id = data['game_id']
    entry.telegram_id = telegram_id
    entry.opponent_name = data['opponent_name']
    entry.color = data['color']
    entry.result = data['result']
    session.add(entry)
    await session.commit()