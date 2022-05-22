from chess.enums import Colors, PieceNames

class Piece:
    def __init__(self, color: Colors, cell) -> None:
        self.cell = cell
        self.color: Colors = color
        self.cell.piece = self
        self.logo = None
        self.name = PieceNames.PIECE
        
    def can_move(self, cell_target) -> bool:
        if cell_target.piece:
            if (cell_target.piece.color == self.color):
                return False
        return True
    
    def get_attack_direction(self):
        pass
    
    def move_piece(self, target) -> None:
        pass