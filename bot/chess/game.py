from typing import List
from uuid import UUID

from .board import Board
from .player import Player


class Game:
    def __init__(self, game_id: UUID, player1: Player, player2: Player) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        
        self.board = Board()
        self.board.add_pieces()
        
        self.is_gameover = False
        
    async def get_active_pieces(player: Player) -> List[str]:
        pass