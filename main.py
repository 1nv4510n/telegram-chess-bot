import chess
import asyncio
import time

b = chess.Board()
b.add_pieces()
b.get_cell_from_pgn('e2').piece = None
b.get_cell_from_pgn('g7').piece = None
b.get_cell_from_pgn('h7').piece = None


b.get_cell_from_pgn('e1').move_piece(b.get_cell_from_pgn('e2'))
b.get_cell_from_pgn('e2').move_piece(b.get_cell_from_pgn('d3'))
b.get_cell_from_pgn('d3').move_piece(b.get_cell_from_pgn('d4'))
b.get_cell_from_pgn('h8').move_piece(b.get_cell_from_pgn('h4'))
#b.get_cell_from_pgn('f8').move_piece(b.get_cell_from_pgn('g7'))
b.get_cell_from_pgn('d1').move_piece(b.get_cell_from_pgn('e1'))
b.get_cell_from_pgn('g2').move_piece(b.get_cell_from_pgn('g3'))

print(b.get_text_board())

print(b.get_cell_from_pgn('d4').piece.check_escape_moves())