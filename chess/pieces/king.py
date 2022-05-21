from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_king.png'
white_logo = 'logo\\white_king.png'

class King(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.KING
        
    def can_move(self, target_cell) -> bool:
        if (not super().can_move(target_cell)):
            return False
        
        dx = abs(self.cell.x - target_cell.x)
        dy = abs(self.cell.y - target_cell.y)
        
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if (check_cell.piece):
                    if (check_cell.piece.color != self.color and (check_cell.piece.name != PieceNames.KING)):
                        if (check_cell.piece.name == PieceNames.PAWN):
                            if (target_cell.to_pgn() in check_cell.piece.get_attack_direction()):
                                return False
                        elif (target_cell.to_pgn() in check_cell.board.highlight_moves(check_cell)):
                            return False
                        
        if ((dx == 1 and dy == 1) or (dx == 0 and dy == 1) or (dx == 1 and dy == 0)):
            return True
        
        return False