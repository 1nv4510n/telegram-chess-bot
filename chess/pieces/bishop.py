from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_bishop.png'
white_logo = 'logo\\white_bishop.png'

class Bishop(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.BISHOP
        
    def can_move(self, target_cell) -> bool:
        if (not super().can_move(target_cell)):
            return False
        else:
            return True