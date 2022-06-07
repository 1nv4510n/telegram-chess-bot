from typing import List
from uuid import UUID

from bot.chess.enums import PieceNames, Colors

from .board import Board
from .player import Player
from .draw import draw_board


class Game:
    def __init__(self, game_id: str, player1: Player, player2: Player) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        
        self.board = Board()
        self.board.add_pieces()
        
        self.current_turn = Colors.WHITE
        
        self.is_gameover = False
        self.game_result = None
    
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
    
    async def get_select_pieces(self, player: Player, icon: str) -> List[str]:
        if self.current_turn == player.color:
            select_pieces: List[str] = []
            
            pieces = self.board.get_pieces(PieceNames.PIECE, player.color, icon=icon)
            
            for piece in pieces:
                select_pieces.append(piece.cell_to_text())
                
            return select_pieces
    
    async def get_targets(self, player: Player, piece: str) -> List[str]:
        if self.current_turn == player.color:
            cell = self.board.get_cell_from_pgn(piece)
            return self.board.highlight_moves(cell)
    
    async def move_piece(self, player: Player, piece: str, target: str) -> bytes:
        if self.current_turn == player.color:
            piece_cell = self.board.get_cell_from_pgn(piece)
            target_cell = self.board.get_cell_from_pgn(target)
            
            piece_cell.move_piece(target_cell)

            self.current_turn = Colors.WHITE if player.color == Colors.BLACK else Colors.BLACK
            
            return await self.get_board_image(player)
            
        