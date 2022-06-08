from typing import List, Optional, Union
from .pieces import *
from .enums import Colors, PieceIcons, PieceNames

class Cell:
    def __init__(self, board, x: int, y: int, color: Colors, piece: Optional[Piece]) -> None:
        self.x: int = x
        self.y: int = y
        self.color: Colors = color
        self.piece: Piece = piece
        self.board: Board = board
        
    #delete in future
    def cell_to_text(self) -> str:
        if (not self.piece):
            return None
        else:
            return f'{self.piece.name.value}{self.to_pgn()}'
        
    def to_pgn(self) -> str:
        size = 7
        horizontal = 'hgfedcba'
        vertical = '12345678'
        return f'{horizontal[size - self.x]}{vertical[size - self.y]}'
        
    def is_empty(self) -> bool:
        if (self.piece):
            if (self.piece.name == PieceNames.KING):
                opposite_color = Colors.BLACK if self.piece.color == Colors.WHITE else Colors.WHITE
                if (self.piece.color == opposite_color):
                    return True
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
    
    def is_empty_diagonal(self, target_cell) -> bool:
        absX = abs(target_cell.x - self.x)
        absY = abs(target_cell.y - self.y)
        
        if (absX != absY):
            return False
        
        dy = 1 if self.y < target_cell.y else -1
        dx = 1 if self.x < target_cell.x else -1
        
        for i in range(1, absY):
            if (not self.board.get_cell(self.x + dx * i, self.y + dy * i).is_empty()):
                return False
        
        return True
    
    def get_path_to_cell(self, target_cell) -> list:
        path = []
        
        absX = abs(target_cell.x - self.x)
        absY = abs(target_cell.y - self.y)
        
        if (self.x == target_cell.x):
            min_y_value = min(self.y, target_cell.y)
            max_y_value = max(self.y, target_cell.y)
            for y in range(min_y_value + 1, max_y_value + 1):
                path.append(self.board.get_cell(self.x, y).to_pgn())
        elif (self.y == target_cell.y):
            min_x_value = min(self.x, target_cell.x)
            max_x_value = max(self.x, target_cell.x)
            for x in range(min_x_value + 1, max_x_value + 1):
                path.append(self.board.get_cell(x, self.y).to_pgn())
        elif (absX == absY): 
            dy = 1 if self.y < target_cell.y else -1
            dx = 1 if self.x < target_cell.x else -1
            
            for i in range(1, absY + 1):
                path.append(self.board.get_cell(self.x + dx * i, self.y + dy * i).to_pgn())
        
        return path
        
    def set_piece(self, piece: Piece):
        self.piece = piece
        self.piece.cell = self
        
    def move_piece(self, target_cell):
        if (self.piece):
            if self.piece.can_move(target_cell):
                target_cell.set_piece(self.piece)
                self.piece = None
                target_cell.piece.move_piece()
                
    def is_attacked(self, opposite_color: Colors) -> bool:
        for i in range(len(self.board.cells)):
            row = self.board.cells[i]
            for j in range(len(row)):
                target_cell = row[j]
                if target_cell.piece and target_cell.piece.color == opposite_color:
                    if target_cell.piece.name == PieceNames.KING:
                        if self.to_pgn() in target_cell.piece.get_attack_direction():
                            return True
                    elif target_cell.piece.name == PieceNames.PAWN:
                        if self.to_pgn() in target_cell.piece.get_attack_direction():
                            return True
                    else:
                        if target_cell.piece.can_move(self):
                            return True
        return False

class Board:
    def __init__(self) -> None:
        self.cells: List[List[Cell]] = []
        
        for i in range(8):
            row: List[Cell] = []
            for j in range(8):
                if ((i + j) % 2 != 0):
                    row.append(Cell(self, j, i, Colors.BLACK, None))
                else:
                    row.append(Cell(self, j, i, Colors.WHITE, None))
            self.cells.append(row)
             
    def get_copy(self) -> None:
        new_board = Board()
        new_board.cells = self.cells
        return new_board
        
    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]
    
    def get_cell_from_pgn(self, pgn: str) -> Cell:
        if len(pgn) == 3:
            pgn = pgn[1:]
        horizontal = 'abcdefgh'
        vertical = '87654321'
        return self.cells[vertical.index(pgn[1])][horizontal.index(pgn[0])]
    
    def highlight_moves(self, selected_cell: Cell) -> List[str]:
        highlited = []
        if (selected_cell.piece):
            if selected_cell.piece.name == PieceNames.KING:
                for move in selected_cell.piece.get_attack_direction():
                    if selected_cell.piece.can_move(self.get_cell_from_pgn(move)):
                        highlited.append(move)
            else:
                for i in range(len(self.cells)):
                    row = self.cells[i]
                    for j in range(len(row)):
                        target_cell = row[j]
                        if selected_cell.piece.can_move(target_cell):
                            highlited.append(target_cell.to_pgn())
        else:
            return None
        
        return highlited
    
    def get_all_moves(self, color: Colors, icon_mode: bool = False) -> List[List[Union[PieceIcons, PieceNames, str]]]:
        moves = []
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                target_cell: Cell
                target_cell = row[j]
                if target_cell.piece and target_cell.piece.color == color:
                    move = self.highlight_moves(target_cell)
                    if move:
                        if icon_mode:
                            moves.append([target_cell.piece.icon, move])
                        else:
                            moves.append([target_cell.piece.name, move])
        return moves
    
    def __add_pawns(self) -> None:
        for i in range(8):
            Pawn(Colors.BLACK, self.get_cell(i, 1))
            Pawn(Colors.WHITE, self.get_cell(i, 6))

    def __add_rooks(self) -> None:
        Rook(Colors.BLACK, self.get_cell(0, 0))
        Rook(Colors.BLACK, self.get_cell(7, 0))
        Rook(Colors.WHITE, self.get_cell(0, 7))
        Rook(Colors.WHITE, self.get_cell(7, 7))
        
    def __add_knights(self) -> None:
        Knight(Colors.BLACK, self.get_cell(1, 0))
        Knight(Colors.BLACK, self.get_cell(6, 0))
        Knight(Colors.WHITE, self.get_cell(1, 7))
        Knight(Colors.WHITE, self.get_cell(6, 7))
        
    def __add_bishops(self) -> None:
        Bishop(Colors.BLACK, self.get_cell(2, 0))
        Bishop(Colors.BLACK, self.get_cell(5, 0))
        Bishop(Colors.WHITE, self.get_cell(2, 7))
        Bishop(Colors.WHITE, self.get_cell(5, 7))
        
    def __add_queens(self) -> None:
        Queen(Colors.BLACK, self.get_cell(3, 0))
        Queen(Colors.WHITE, self.get_cell(3, 7))
        
    def __add_kings(self) -> None:
        King(Colors.BLACK, self.get_cell(4, 0))
        King(Colors.WHITE, self.get_cell(4, 7))
        
    def add_pieces(self) -> None:
        self.__add_pawns()
        self.__add_rooks()
        self.__add_knights()
        self.__add_bishops()
        self.__add_queens()
        self.__add_kings()
        
    def get_pieces(self, name: PieceNames, color: Colors, icon: str = None) -> List[Cell]:
        piece_list = []
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if not icon:
                    if (check_cell.piece and check_cell.piece.color == color and check_cell.piece.name == name):
                        piece_list.append(check_cell)
                else:
                    if (check_cell.piece and check_cell.piece.color == color and check_cell.piece.icon.value == icon):
                        piece_list.append(check_cell)
        return piece_list
    
    def king_is_under_check(self, color: Colors) -> List[Cell]:
        check_pieces = []
        king = self.get_pieces(PieceNames.KING, color)[0]
        for i in range(len(self.cells)):
            row = self.cells[i]
            for j in range(len(row)):
                check_cell = row[j]
                if (check_cell.piece):
                    if (check_cell.piece.color != color and (check_cell.piece.name != PieceNames.KING)):
                        if (check_cell.piece.name == PieceNames.PAWN):
                            if (king.to_pgn() in check_cell.piece.get_attack_direction()):
                                check_pieces.append(check_cell)
                        elif (king.to_pgn() in check_cell.board.highlight_moves(check_cell)):
                            check_pieces.append(check_cell)
                            
        return check_pieces
    
    def king_escape_moves(self, color: Colors) -> List[List[Union[Cell, str]]]:
        king = self.get_pieces(PieceNames.KING, color)[0]
        check_source = self.king_is_under_check(color)
        if check_source:
            escape_moves = []
            king_moves = self.highlight_moves(king)
            if king_moves:
                king_moves.insert(0, king)
                escape_moves.append(king_moves)
            if len(check_source) == 1:
                attack_lines = []    
                for attacker in check_source:
                    if attacker.piece.name == PieceNames.KNIGHT:
                        attack_lines.append(attacker.to_pgn())
                    elif attacker.piece.name == PieceNames.PAWN:
                        attack_lines.append(attacker.to_pgn())
                    else:
                        attack_lines += king.get_path_to_cell(attacker)
                
                for i in range(len(self.cells)):
                    row = self.cells[i]
                    for j in range(len(row)):
                        check_cell = row[j]
                        if check_cell.piece:
                            if check_cell.piece.color == color and check_cell.piece.name != PieceNames.KING:
                                check_cell_moves = check_cell.board.highlight_moves(check_cell)
                                for move in check_cell_moves:
                                    if move in attack_lines:
                                        escape_moves.append([check_cell, move])
                                        break
                return escape_moves
            else:
                return escape_moves
        else:
            return None
        
    def is_checkmate(self, color: Colors) -> bool:
        if self.king_escape_moves(color) == []:
            return True
        return False
    
    def is_stalemate(self, color: Colors) -> bool:
        if self.king_is_under_check(color) == [] and self.get_all_moves(color) == []:
            return True
        return False