from chess.enums import Colors, PieceNames
from .piece import Piece
from .queen import Queen

black_logo = 'logo\\black_pawn.png'
white_logo = 'logo\\white_pawn.png'

class Pawn(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.name = PieceNames.PAWN
        
        self.is_first_step = True
        
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False
        
        if (self.cell.piece):
            direction = 1 if self.cell.piece.color == Colors.BLACK else -1
            first_step_direction = 2 if self.cell.piece.color == Colors.BLACK else -2
        
            if ((target_cell.y == self.cell.y + direction or (self.is_first_step and (target_cell.y == self.cell.y + first_step_direction))) 
                and target_cell.x == self.cell.x 
                and self.cell.board.get_cell(target_cell.x, target_cell.y).is_empty()):
                return True
            
            if (target_cell.y == self.cell.y + direction 
                and ((target_cell.x == self.cell.x + 1 or target_cell.x == self.cell.x - 1)
                and self.cell.is_enemy(target_cell))):
                return True
            
            return False
        
    def get_attack_direction(self):
        direction = 1 if self.cell.piece.color == Colors.BLACK else -1
        pos = []
        add_func = lambda x_offset: self.cell.board.get_cell(self.cell.x + x_offset, self.cell.y + direction).to_pgn()
        if self.cell.x == 0:
            pos.append(add_func(1))
        elif self.cell.x == 7:
            pos.append(add_func(-1))
        else:
            pos.append(add_func(-1))
            pos.append(add_func(1))       
        
        return pos 
            

    def move_piece(self) -> None:
        super().move_piece()
        self.is_first_step = False
        
        if (self.color == Colors.BLACK and self.cell.y == 7):
            self.cell = Queen(Colors.BLACK, self.cell)
            
        if (self.color == Colors.WHITE and self.cell.y == 0):
            self.cell = Queen(Colors.WHITE, self.cell)