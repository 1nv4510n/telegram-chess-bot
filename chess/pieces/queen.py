from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_queen.png'
white_logo = 'logo\\white_queen.png'

class Queen(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.QUEEN
        
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False
        if (self.cell.is_empty_vertical(target_cell)):
            return True
        if (self.cell.is_empty_horizontal(target_cell)):
            return True
        if(self.cell.is_empty_diagonal(target_cell)):
            return True
        return False