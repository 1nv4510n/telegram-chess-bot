from typing import Dict, List, Union
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession

from bot.db.requests import change_user_rating
from bot.chess.player import Player
from bot.chess.enums import ChessStatus


async def make_game_dict(game_id: UUID, opponent_name: str, color: str, result: str) -> Dict:
    game_dict = {
        'game_id' : game_id,
        'opponent_name' : opponent_name,
        'color' : color,
        'result' : result
    }
    return game_dict

def get_coefficient(rating: int) -> int:
    if rating < 2100: return 32
    if rating >= 2100 and rating <= 2400: return 24
    if rating > 2400: return 16

def get_result_score(status: ChessStatus) -> float:
    if status == ChessStatus.WIN: return 1
    if status == ChessStatus.DRAW: return 0.5
    if status == ChessStatus.LOSE: return 0

async def change_user_ratings(session: AsyncSession, playerA: Player, playerB: Player) -> List[List[Union[float, int]]]:
    expected_scoreA = lambda ratingA, ratingB: 1 / (1 + 10 ** ((ratingB - ratingA) / 400))
    expected_scoreB = lambda ratingA, ratingB: 1 / (1 + 10 ** ((ratingA - ratingB) / 400))
    
    total_earnA: float = round(get_coefficient(playerA.rating) * (get_result_score(playerA.status) - expected_scoreA(playerA.rating, playerB.rating)), 2)
    total_earnB: float = round(get_coefficient(playerB.rating) * (get_result_score(playerB.status) - expected_scoreB(playerA.rating, playerB.rating)), 2)
    await change_user_rating(session, playerA.id, total_earnA)
    await change_user_rating(session, playerB.id, total_earnB)
    new_ratingA = round(playerA.rating + total_earnA)
    new_ratingB = round(playerB.rating + total_earnB)
    return [
        [round(total_earnA, 1), new_ratingA],
        [round(total_earnB, 1), new_ratingB]
    ]