from enum import Enum

class Colors(Enum):
    WHITE = 'w'
    BLACK = 'b'
    
class PieceNames(Enum):
    PIECE = 'Piece'
    KING = 'K'
    KNIGHT = 'N'
    PAWN = 'P'
    QUEEN = 'Q'
    ROOK = 'R'
    BISHOP = 'B'