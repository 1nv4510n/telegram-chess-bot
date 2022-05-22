from glob import escape
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
    
    def is_under_check(self) -> list:
        check_pieces = []
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if (check_cell.piece):
                    if (check_cell.piece.color != self.color and (check_cell.piece.name != PieceNames.KING)):
                        if (check_cell.piece.name == PieceNames.PAWN):
                            if (self.cell.to_pgn() in check_cell.piece.get_attack_direction()):
                                check_pieces.append(check_cell)
                        elif (self.cell.to_pgn() in check_cell.board.highlight_moves(check_cell)):
                            check_pieces.append(check_cell)
                            
        return check_pieces
    
    def check_escape_moves(self) -> list:
        check_source = self.is_under_check()
        if check_source:
            escape_moves = []
            escape_moves.append([self.name, self.cell.board.highlight_moves(self.cell)])
            if (len(check_source) == 1):
                attack_lines = []    
                for attacker in check_source:
                    if attacker.piece.name == PieceNames.KNIGHT:
                        attack_lines.append(attacker.to_pgn())
                    elif attacker.piece.name == PieceNames.PAWN:
                        attack_lines.append(attacker.to_pgn())
                    else:
                        attack_lines += self.cell.get_path_to_cell(attacker)
                
                for i in range(len(self.cell.board.cells)):
                    row = self.cell.board.cells[i]
                    for j in range(len(row)):
                        check_cell = row[j]
                        if check_cell.piece:
                            if check_cell.piece.color == self.color and check_cell.piece.name != PieceNames.KING:
                                check_cell_moves = check_cell.board.highlight_moves(check_cell)
                                for move in check_cell_moves:
                                    if move in attack_lines:
                                        escape_moves.append([check_cell.piece.name.value, move])
                return escape_moves
            else:
                return escape_moves
        else:
            return None