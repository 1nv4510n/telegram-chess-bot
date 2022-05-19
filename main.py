import chess

b = chess.Board()
b.add_pieces()

print(b.get_cell(0, 1).move_piece(b.get_cell(4, 7)))
print(b.get_text_board())