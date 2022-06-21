from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.search_filter import UserPlayingFilter, UserSearchingFilter
from bot.chess.enums import ChessStatus

from bot.db.models import GamesHistoryEntry
from bot.db.requests import get_game_history, get_user_rating

router = Router()

@router.message(UserPlayingFilter(playing=False), UserSearchingFilter(searching=False), F.text == 'Statistics')
@router.message(UserPlayingFilter(playing=False), UserSearchingFilter(searching=False), commands=['stats'])
async def command_stats(message: Message, session: AsyncSession):
    games = await get_game_history(session, message.from_user.id)
    rating = await get_user_rating(session, message.from_user.id)
    stats = {'rating' : round(rating), 'win': 0, 'draw' : 0, 'lose' : 0}
    
    game: GamesHistoryEntry
    for game in games:
        if game.result == ChessStatus.WIN.value:
            stats['win'] += 1
        elif game.result == ChessStatus.DRAW.value:
            stats['draw'] += 1
        elif game.result == ChessStatus.LOSE.value:
            stats['lose'] += 1
    stats['total_games'] = stats['win'] + stats['draw'] + stats['lose']
    if not stats['total_games'] == 0:
        if stats['lose'] == 0 and stats['draw'] == 0:
            stats['winrate'] = 100
        else:
            stats['winrate'] = round(stats['win'] / stats['total_games'] * 100)
    else:
        stats['winrate'] = 0
        
    stats_text = (f"Statistics for player <b>{message.from_user.first_name}</b>\n\n"
                  f"<b>Your rating: {stats['rating']}</b>\n\n"
                  f"Total games: <b>{stats['total_games']}</b> \nWinrate: <b>{stats['winrate']} %</b>\n\n"
                  f"Wins: <b>{stats['win']}</b> | Draws: <b>{stats['draw']}</b> | Loses: <b>{stats['lose']}</b>")
    await message.answer(stats_text)
    
    if stats['total_games'] >= 1:
        games.reverse()
        i = 1
        games_text = "<b>Your previous games:</b>\n\n"
        for game in games:
            games_text += f"{i}. <b>{message.from_user.first_name} vs {game.opponent_name} ({round(game.opponent_rating)})</b> <b>{game.result}</b>\n\n"
            i += 1
            if i > 10:
                break

        await message.answer(games_text)
    