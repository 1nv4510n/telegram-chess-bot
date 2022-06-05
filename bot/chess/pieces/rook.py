from bot.chess.enums import Colors, PieceIcons, PieceNames
from .piece import Piece

black_logo = 'logo\\black_rook.png'
white_logo = 'logo\\white_rook.png'

class Rook(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.icon = PieceIcons.ROOK
        self.name = PieceNames.ROOK
        
        self.is_first_step = True
        
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False
        if (self.cell.is_empty_vertical(target_cell)):
            return True
        if (self.cell.is_empty_horizontal(target_cell)):
            return True
        return False
    
    def move_piece(self) -> None:
        super().move_piece()
        self.is_first_step = False