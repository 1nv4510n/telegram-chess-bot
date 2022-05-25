from glob import escape
from tabnanny import check
from chess.enums import Colors, PieceNames
from .piece import Piece

black_logo = 'logo\\black_king.png'
white_logo = 'logo\\white_king.png'

class King(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.KING
        
        self.is_first_step = True
         
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False
        
        dx = abs(self.cell.x - target_cell.x)
        dy = abs(self.cell.y - target_cell.y)
        
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if (check_cell.piece and check_cell.piece.color != self.color):
                    if check_cell.piece.name == PieceNames.KING:
                        if target_cell.to_pgn() in check_cell.piece.get_attack_direction():
                            return False
                    else:
                        if target_cell.piece and target_cell.piece.is_supported():
                            return False
                        else:
                            if (check_cell.piece.name == PieceNames.PAWN):
                                if (target_cell.to_pgn() in check_cell.piece.get_attack_direction()):
                                    return False
                            elif (target_cell.to_pgn() in check_cell.board.highlight_moves(check_cell)):
                                return False
                            
        if (self.is_first_step):
            if self.color == Colors.WHITE:
                if self.cell.board.get_cell(0, 7).piece and self.cell.board.get_cell(0, 7).piece.name == PieceNames.ROOK:
                    pass
                            
        if ((dx == 1 and dy == 1) or (dx == 0 and dy == 1) or (dx == 1 and dy == 0)):
            return True
        
        return False
    
    def get_attack_direction(self):
        pos = []
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                dx = abs(self.cell.x - check_cell.x)
                dy = abs(self.cell.y - check_cell.y)
                if (dx >= 2 or dy >= 2):
                    continue
                if ((dx == 1 and dy == 1) or (dx == 0 and dy == 1) or (dx == 1 and dy == 0)):
                    pos.append(check_cell.to_pgn())
        return pos
    
    def move_piece(self) -> None:
        self.is_first_step = False