from chess.enums import Colors, PieceNames

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

        my_king = self.cell.board.get_pieces(PieceNames.KING, self.color)[0]

        if self.name != PieceNames.KING and not support_check:
            opposite_color = Colors.BLACK if self.color == Colors.WHITE else Colors.WHITE
            
            enemy_bishops = self.cell.board.get_pieces(PieceNames.BISHOP, opposite_color)
            enemy_rooks = self.cell.board.get_pieces(PieceNames.ROOK, opposite_color)
            enemy_queen = self.cell.board.get_pieces(PieceNames.QUEEN, opposite_color)
            
            if (my_king.is_empty_horizontal(self.cell)):
                for queen in enemy_queen:
                    if self.cell.is_empty_horizontal(queen):
                        return False   
                for rook in enemy_rooks:
                    if (self.cell.is_empty_horizontal(rook)):
                        return False 
                    
            if my_king.is_empty_vertical(self.cell):
                for queen in enemy_queen:
                    if self.cell.is_empty_vertical(queen):
                        return False
                for rook in enemy_rooks:
                    if self.cell.is_empty_vertical(rook):
                        return False
                    
            if my_king.is_empty_diagonal(self.cell):
                for queen in enemy_queen:
                    if self.cell.is_empty_diagonal(queen):
                        return False
                for bishop in enemy_bishops:
                    if self.cell.is_empty_diagonal(bishop):
                        return False     
        return True
    
    def is_supported(self) -> bool:
        for i in range(len(self.cell.board.cells)):
            row = self.cell.board.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if check_cell.piece and check_cell.piece.color == self.color and check_cell.piece.name != PieceNames.KING:
                    if check_cell.piece.can_move(self.cell, support_check = True):
                        return True
        return False
    
    def get_attack_direction(self):
        pass
    
    def move_piece(self) -> None:
        pass