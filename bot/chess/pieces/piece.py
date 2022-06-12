from bot.chess.enums import Colors, PieceNames

class Piece:
    def __init__(self, color: Colors, cell) -> None:
        self.cell = cell
        self.color: Colors = color
        self.cell.piece = self
        self.logo = None
        self.icon = None
        self.name = PieceNames.PIECE
        
    def can_move(self, cell_target, support_check = False) -> bool:
        if not support_check:
            if cell_target.piece and cell_target.piece.color == self.color:
                return False
            if cell_target.piece and cell_target.piece.name == PieceNames.KING:
                return False

        if not support_check and self.name != PieceNames.KING:    
            my_king = self.cell.board.get_pieces(PieceNames.KING, self.color)[0]    
            
            opposite_color = Colors.BLACK if self.color == Colors.WHITE else Colors.WHITE

            enemy_bishops = self.cell.board.get_pieces(PieceNames.BISHOP, opposite_color)
            enemy_rooks = self.cell.board.get_pieces(PieceNames.ROOK, opposite_color)
            enemy_queen = self.cell.board.get_pieces(PieceNames.QUEEN, opposite_color)

            if (self.cell.is_empty_horizontal(my_king)):
                for queen in enemy_queen:
                    if self.cell.is_empty_horizontal(queen):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.ROOK) and cell_target.to_pgn() not in self.cell.get_path_to_cell(queen):
                            return False          
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT, PieceNames.PAWN]:
                            return False
                        
                for rook in enemy_rooks:
                    if (self.cell.is_empty_horizontal(rook)):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.ROOK) and cell_target.to_pgn() not in self.cell.get_path_to_cell(rook):
                            return False
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT, PieceNames.PAWN]:
                            return False
                    
            if self.cell.is_empty_vertical(my_king):
                for queen in enemy_queen:
                    if self.cell.is_empty_vertical(queen):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.ROOK) and cell_target.to_pgn() not in self.cell.get_path_to_cell(queen):
                            return False
                        if self.name == PieceNames.PAWN:
                            if cell_target.to_pgn() in self.get_attack_direction():
                                return False                        
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT]:
                            return False
                for rook in enemy_rooks:
                    if self.cell.is_empty_vertical(rook):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.ROOK) and cell_target.to_pgn() not in self.cell.get_path_to_cell(rook):
                            return False
                        if self.name == PieceNames.PAWN:
                            if cell_target.to_pgn() in self.get_attack_direction():
                                return False                        
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT]:
                            return False
                        
            if self.cell.is_empty_diagonal(my_king):
                for queen in enemy_queen:
                    if self.cell.is_empty_diagonal(queen):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.BISHOP) and cell_target.to_pgn() not in self.cell.get_path_to_cell(queen):
                            return False
                        if self.name == PieceNames.PAWN:
                            if cell_target == queen and queen.to_pgn() in self.get_attack_direction():
                                return True
                            else:
                                return False
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT]:
                            return False
                for bishop in enemy_bishops:
                    if self.cell.is_empty_diagonal(bishop):
                        if (self.name == PieceNames.QUEEN or self.name == PieceNames.BISHOP) and cell_target.to_pgn() not in self.cell.get_path_to_cell(bishop):
                            return False
                        if self.name == PieceNames.PAWN:
                            if cell_target == bishop and bishop.to_pgn() in self.get_attack_direction():
                                return True
                            else:
                                return False
                        if self.name in [PieceNames.BISHOP, PieceNames.KNIGHT]:
                            return False
        return True
    
    def is_supported(self) -> bool:
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if (check_cell.piece 
                    and check_cell.piece.color == self.color 
                    and check_cell.piece.name != PieceNames.KING 
                    and check_cell != self.cell):
                    if check_cell.piece.can_move(self.cell, support_check = True):
                        return True
        return False
    
    def get_attack_direction(self):
        pass
    
    def move_piece(self) -> None:
        pass