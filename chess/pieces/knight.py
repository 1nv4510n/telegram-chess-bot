from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_knight.png'
white_logo = 'logo\\white_knight.png'

class Knight(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.KNIGHT
        
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False

        dx = abs(self.cell.x - target_cell.x)
        dy = abs(self.cell.y - target_cell.y)
        
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)