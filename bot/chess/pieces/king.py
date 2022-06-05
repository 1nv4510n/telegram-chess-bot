from bot.chess.enums import Colors, PieceIcons, PieceNames
from .piece import Piece

black_logo = 'logo\\black_king.png'
white_logo = 'logo\\white_king.png'

class King(Piece):
    def __init__(self, color: Colors, cell) -> None:
        super().__init__(color, cell)
        self.logo = black_logo if color == Colors.BLACK else white_logo
        self.icon = PieceIcons.KING
        self.name = PieceNames.KING
        
        self.is_first_step = True
        
    def castling(self, from_cell, to_cell):
        to_cell.piece = from_cell.piece
        to_cell.piece.cell = to_cell
        from_cell.piece = None
    
    def can_move(self, target_cell, support_check = False) -> bool:
        if (not super().can_move(target_cell, support_check)):
            return False
        
        dx = abs(self.cell.x - target_cell.x)
        dy = abs(self.cell.y - target_cell.y)
        
        enemy_color = Colors.BLACK if self.color == Colors.WHITE else Colors.WHITE
        
        if target_cell.is_attacked(enemy_color):
            return False
        if target_cell.piece and target_cell.piece.is_supported():
            return False
          
        if (self.is_first_step and self.cell.board.king_is_under_check(self.color) == []):
            rooks = self.cell.board.get_pieces(PieceNames.ROOK, self.color)
            for rook in rooks:
                if rook.piece.is_first_step == True:
                    if rook.x == 0 and self.cell.is_empty_horizontal(rook):
                        if target_cell.to_pgn() == 'c1' and not self.cell.board.get_cell(2, 7).is_attacked(enemy_color):
                            return True
                                
                        if target_cell.to_pgn() == 'c8' and not self.cell.board.get_cell(2, 0).is_attacked(enemy_color):
                            return True
                                
                    if rook.x == 7 and self.cell.is_empty_horizontal(rook):
                        if target_cell.to_pgn() == 'g1' and not self.cell.board.get_cell(6, 7).is_attacked(enemy_color):
                            return True
                        
                        if target_cell.to_pgn() == 'g8' and not self.cell.board.get_cell(6, 0).is_attacked(enemy_color):
                            return True
                        
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
        if self.is_first_step:
            if self.color == Colors.BLACK:
                pos += ['c8', 'g8']
            else:
                pos += ['c1', 'g1']
        return pos
    
    def move_piece(self) -> None:
        if self.is_first_step:
            y = 0 if self.color == Colors.BLACK else 7
            if self.cell.x == 6:
                self.castling(self.cell.board.get_cell(7, y), self.cell.board.get_cell(5, y))
            if self.cell.x == 2:
                self.castling(self.cell.board.get_cell(0, y), self.cell.board.get_cell(3, y))
        self.is_first_step = False