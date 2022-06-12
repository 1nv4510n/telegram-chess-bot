from typing import Dict, List
from contextlib import suppress
from uuid import UUID

from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from bot.db.models import GamesHistoryEntry, PlayersEntry

#get data methods

async def get_game_history(session: AsyncSession, telegram_id: int) -> List[GamesHistoryEntry]:
    game_data_request = await session.execute(
        select(GamesHistoryEntry).where(GamesHistoryEntry.telegram_id == telegram_id).limit(500)
    )
    return game_data_request.scalars().all()

async def get_top_users(session: AsyncSession) -> List[PlayersEntry]:
    users_data = await session.execute(
        select(PlayersEntry).order_by(desc(PlayersEntry.rating)).limit(15)
    )
    return users_data.scalars().all()

async def get_leaderboard_position(session: AsyncSession, telegram_id: int) -> int:
    users_data = await session.execute(
        select(PlayersEntry).order_by(desc(PlayersEntry.rating))
    )
    top_users = users_data.scalars().all()
    
    i = 1
    user: PlayersEntry
    for user in top_users:
        if user.telegram_id == telegram_id:
            return i
        i += 1
        
async def is_user_exists(session: AsyncSession, telegram_id: int) -> bool:
    request = await session.execute(
        select(PlayersEntry).filter_by(telegram_id=telegram_id)
    )
    return request.scalars().first() is not None

async def get_searching_users(session: AsyncSession) -> List[PlayersEntry]:
    searching_data = await session.execute(
        select(PlayersEntry).where(PlayersEntry.searching == True)
    )
    
    return searching_data.scalars().all()

async def get_user_rating(session: AsyncSession, telegram_id: int) -> float:
    user_rating = await session.execute(
        select(PlayersEntry.rating).where(PlayersEntry.telegram_id == telegram_id)
    )
    return user_rating.scalar()

#modify data methods

async def update_user_data(session: AsyncSession, telegram_id: int,
                           searching: bool, playing: bool, game_id: UUID = None, name: str = None) -> None:
    if name is None:
        await session.execute(
            update(PlayersEntry).where(PlayersEntry.telegram_id == telegram_id).values(
                searching=searching, playing=playing, game_id = game_id
            )
        )
    else:
        await session.execute(
            update(PlayersEntry).where(PlayersEntry.telegram_id == telegram_id).values(
                name=name, searching=searching, playing=playing, game_id = game_id
            )
        )
    with suppress(IntegrityError):
        await session.commit()

async def change_user_rating(session: AsyncSession, telegram_id: int, offset: float) -> None:
    await session.execute(
        update(PlayersEntry).where(PlayersEntry.telegram_id == telegram_id).values(
            rating=PlayersEntry.rating + offset
        )
    )
    with suppress(IntegrityError):
        await session.commit()
        
async def reset_users_table(session: AsyncSession) -> None:
    await session.execute(
        update(PlayersEntry).values(searching=False, playing=False, game_id = None)
    )
    await session.commit()

async def add_user(session: AsyncSession, telegram_id: int, name: str) -> None:
    entry = PlayersEntry()
    entry.telegram_id = telegram_id
    entry.name = name
    entry.searching = False
    entry.playing = False
    entry.rating = 1000
    session.add(entry)
    with suppress(IntegrityError):
        await session.commit()
    
async def log_game(session: AsyncSession, data: Dict, telegram_id: int) -> None:
    entry = GamesHistoryEntry()
    entry.game_id = data['game_id']
    entry.telegram_id = telegram_id
    entry.opponent_name = data['opponent_name']
    entry.opponent_rating = data['opponent_rating']
    entry.result = data['result']
    session.add(entry)
    with suppress(IntegrityError):
        await session.commit()