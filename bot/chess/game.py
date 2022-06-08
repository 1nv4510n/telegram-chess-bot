from typing import List
from uuid import UUID

from bot.chess.enums import PieceIcons, PieceNames, Colors, ChessStatus

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
        
        self.current_turn: Player = player1 if player1.color == Colors.WHITE else player2
        
        self.is_gameover = False
    
    async def get_board_image(self, player: Player) -> bytes:
        turn_over = False if player.color == Colors.WHITE else True
        return draw_board(self.board, turn_over)
    
    async def get_active_pieces(self) -> List[PieceIcons]:
        active_pieces: List[PieceIcons] = []
        
        color = self.current_turn.color
        all_moves = self.board.get_all_moves(color, icon_mode=True)
        
        for moves in all_moves:
            if moves[0] not in active_pieces:
                active_pieces.append(moves[0])
                
        return active_pieces
    
    async def get_select_pieces(self, icon: str) -> List[str]:
        select_pieces: List[str] = []
        
        pieces = self.board.get_pieces(PieceNames.PIECE, self.current_turn.color, icon=icon)
        
        for piece in pieces:
            if not self.board.highlight_moves(piece) == []:
                select_pieces.append(piece.cell_to_text())
            
        return select_pieces
    
    async def get_targets(self, piece: str) -> List[str]:
        cell = self.board.get_cell_from_pgn(piece)
        return self.board.highlight_moves(cell)
    
    async def get_check_icons(self) -> List[PieceIcons]:
        active_icons: List[PieceIcons] = []
        
        escape_moves = self.board.king_escape_moves(self.current_turn.color)
        for move in escape_moves:
            icon = move[0].piece.icon
            if icon not in active_icons:
                active_icons.append(icon)
                
        return active_icons
    
    async def get_check_escape_moves(self, icon: str) -> List[str]:
        check_escape_moves: List[str] = []
        escape_moves = self.board.king_escape_moves(self.current_turn.color)
        
        for move in escape_moves:
            if move[0].piece.icon.value == icon:
                escape_move = move[0].cell_to_text()
                for target in move[1:]:
                    check_escape_moves.append(f"{escape_move}-{target}")
        return check_escape_moves
    
    async def move_piece(self, piece: str, target: str) -> bytes:
        piece_cell = self.board.get_cell_from_pgn(piece)
        target_cell = self.board.get_cell_from_pgn(target)
        
        piece_cell.move_piece(target_cell)
        
        current_board = await self.get_board_image(self.current_turn)
        self.current_turn = self.player1 if self.current_turn == self.player2 else self.player2
        
        if self.board.king_is_under_check(self.current_turn.color):
            self.current_turn.status = ChessStatus.CHECK
        
        return current_board
            
        