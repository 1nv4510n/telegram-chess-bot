from typing import List
from uuid import UUID

from bot.chess.enums import PieceIcons, PieceNames, Colors

from .board import Board, Cell
from .player import Player
from .draw import draw_board


class Game:
    def __init__(self, game_id: str, player1: Player, player2: Player) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        
        self.board = Board()
        self.board.add_pieces()
        
        self.is_gameover = False
    
    async def get_board_image(self, player: Player) -> bytes:
        turn_over = False if player.color == Colors.WHITE else True
        return draw_board(self.board, turn_over)
    
    async def get_active_pieces(self, player: Player) -> List[str]:
        active_pieces: List[str] = []
        
        color = player.color
        all_moves = self.board.get_all_moves(color, icon_mode=True)
        
        for moves in all_moves:
            if moves[0] not in active_pieces:
                active_pieces.append(moves[0])
                
        return active_pieces
    
    async def select_pieces(self, player: Player, icon: PieceIcons) -> List[str]:
        select_pieces: List[str] = []
        
        color = player.color
        pieces = self.board.get_pieces(PieceNames.PIECE, color, icon=icon)
        
        for piece in pieces:
            select_pieces.append(piece.cell_to_text())
            
        return select_pieces
    
    async def highlight_moves(self, player: Player, piece: str) -> List[str]:
        cell = self.board.get_cell_from_pgn(piece)
        return self.board.highlight_moves(cell)
    
    async def move_piece(self, player: Player, piece: str, target: str) -> None:
        pass