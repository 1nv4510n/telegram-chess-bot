from typing import List, Optional
from .pieces import *
from .enums import Colors, PieceNames

class Board:
    def __init__(self) -> None:
        self.cells: List[Cell] = []
        
        for i in range(8):
            row: List[Cell] = []
            for j in range(8):
                if ((i + j) % 2 != 0):
                    row.append(Cell(self, j, i, Colors.BLACK, None))
                else:
                    row.append(Cell(self, j, i, Colors.WHITE, None))
            self.cells.append(row)
        
    def get_cell(self, x: int, y: int) -> any:
        return self.cells[y][x]
    
    def get_copy_board(self):
        new_board = Board()
        new_board.cells = self.cells
        return new_board
    
    def __add_pawns(self):
        for i in range(8):
            Pawn(Colors.BLACK, self.get_cell(i, 1))
            Pawn(Colors.WHITE, self.get_cell(i, 6))

    def __add_rooks(self):
        Rook(Colors.BLACK, self.get_cell(0, 0))
        Rook(Colors.BLACK, self.get_cell(7, 0))
        Rook(Colors.WHITE, self.get_cell(0, 7))
        Rook(Colors.WHITE, self.get_cell(7, 7))
        
    def __add_knights(self):
        Knight(Colors.BLACK, self.get_cell(1, 0))
        Knight(Colors.BLACK, self.get_cell(6, 0))
        Knight(Colors.WHITE, self.get_cell(1, 7))
        Knight(Colors.WHITE, self.get_cell(6, 7))
        
    def __add_bishops(self):
        Bishop(Colors.BLACK, self.get_cell(2, 0))
        Bishop(Colors.BLACK, self.get_cell(5, 0))
        Bishop(Colors.WHITE, self.get_cell(2, 7))
        Bishop(Colors.WHITE, self.get_cell(5, 7))
        
    def __add_queens(self):
        Queen(Colors.BLACK, self.get_cell(3, 0))
        Queen(Colors.WHITE, self.get_cell(3, 7))
        
    def __add_kings(self):
        King(Colors.BLACK, self.get_cell(4, 0))
        King(Colors.WHITE, self.get_cell(4, 7))
        
    def add_pieces(self):
        self.__add_pawns()
        self.__add_rooks()
        self.__add_knights()
        self.__add_bishops()
        self.__add_queens()
        self.__add_kings()
        
    
    def get_text_board(self) -> str:
        text_board = ''
        for i in range(8):
            text_board += f'{i} ['
            for j in range(8):
                text_board += f'{self.get_cell(j, i).to_text()} '
            text_board += ']\n'
        text_board += 'X: 0  1  2  3  4  5  6  7'
        return text_board
    
class Cell:
    def __init__(self, board: Board, x: int, y: int, color: Colors, piece: Optional[Piece]) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.piece = piece
        self.board = board
        self.available = False

    def to_text(self) -> str:
        if (not self.piece):
            return '--'
        else:
            return f'{self.piece.color.value}{self.piece.name.value}'
        
    def is_empty(self) -> bool:
        return self.piece == None
    
    def is_enemy(self, target_cell) -> bool:
        if (target_cell.piece):
            return self.piece.color != target_cell.piece.color
        return False
    
    def is_empty_vertical(self, target_cell) -> bool:
        if (self.x != target_cell.x):
            return False
        
        min_value = min(self.y, target_cell.y)
        max_value = max(self.y, target_cell.y)
        for y in range(min_value + 1, max_value):
            if (not self.board.get_cell(self.x, y).is_empty()):
                return False
        return True
    
    def is_empty_horizontal(self, target_cell) -> bool:
        if (self.y != target_cell.y):
            return False
        
        min_value = min(self.x, target_cell.x)
        max_value = max(self.x, target_cell.x)
        for x in range(min_value + 1, max_value):
            if (not self.board.get_cell(x, self.y).is_empty()):
                return False
        return True
    
    def set_piece(self, piece: Piece):
        self.piece = piece
        self.piece.cell = self
        
    def move_piece(self, target_cell):
        if (self.piece):
            if self.piece.can_move(target_cell):
                self.piece.move_piece(target_cell)
                target_cell.set_piece(self.piece)
                self.piece = None