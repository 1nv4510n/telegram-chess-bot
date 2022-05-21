import chess
import asyncio
import time

b = chess.Board()
b.add_pieces()
b.get_cell_from_pgn('e7').piece = None
b.get_cell_from_pgn('e2').piece = None

b.get_cell_from_pgn('e1').move_piece(b.get_cell_from_pgn('e2'))
b.get_cell_from_pgn('d8').move_piece(b.get_cell_from_pgn('e7'))
print(b.highlight_moves(b.get_cell_from_pgn('e2')))

print(b.get_text_board())