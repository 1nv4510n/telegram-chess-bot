import chess
import asyncio
import time

from chess.enums import PieceNames, Colors

b = chess.Board()
b.add_pieces()
timer = time.time()
# b.get_cell_from_pgn('e7').piece = None
# b.get_cell_from_pgn('e2').piece = None
# b.get_cell_from_pgn('d8').piece = None


# print(b.highlight_moves(b.get_cell_from_pgn('e8')))
print(b.get_all_moves(Colors.WHITE))


print(b.get_text_board())
print(time.time() - timer)