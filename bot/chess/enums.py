from enum import Enum

class Colors(Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'
    
class PieceNames(Enum):
    PIECE = 'Piece'
    KING = 'K'
    KNIGHT = 'N'
    PAWN = ''
    QUEEN = 'Q'
    ROOK = 'R'
    BISHOP = 'B'
    
class PieceIcons(Enum):
    KING = '♚'
    KNIGHT = '♞'
    PAWN = '♟'
    QUEEN = '♛'
    ROOK = '♜'
    BISHOP = '♝'
    
class ChessStatus(Enum):
    CHECK = 'CHECK'
    CHECKMATE = 'CHECKMATE'
    STALEMATE = 'STALEMATE'
    RESIGN = 'RESIGN'
    DRAW = 'DRAW'
    WIN = 'WIN'
    LOSE = 'LOSE'
    
class BoardParam(Enum):
    BOARD_SIZE = 8
    CELL_SIZE = 80
    OFFSET_X = 38
    OFFSET_Y = 38
    ROTATE_OFFSET_X = 40
    ROTATE_OFFSET_Y = 40