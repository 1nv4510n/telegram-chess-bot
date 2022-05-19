from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_rook.png'
white_logo = 'logo\\white_rook.png'

class Rook(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.ROOK
        
    def can_move(self, target_cell) -> bool:
        if (not super().can_move(target_cell)):
            return False
        else:
            return True