import chess

b = chess.Board()
b.add_pieces()
b.get_cell(3, 1).move_piece(b.get_cell(0, 7))
b.get_cell(3, 0).move_piece(b.get_cell(3, 4))
b.get_cell(3, 4).move_piece(b.get_cell(2, 3))
b.get_cell(2, 3).move_piece(b.get_cell(7, 3))
print(b.get_text_board())