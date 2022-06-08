import asyncio

from bot import __main__

# from bot.chess.board import Board
# from bot.chess.draw import draw_board

# board = Board()
# board.add_pieces()
# draw_board(board, False)

asyncio.run(__main__.main())

# from bot.chess import Board
# from bot.chess.enums import Colors, PieceNames

# b = Board()
# b.add_pieces()

# b.get_cell_from_pgn('e2').move_piece(b.get_cell_from_pgn('e4'))
# b.get_cell_from_pgn('f1').move_piece(b.get_cell_from_pgn('b5'))
# print(b.get_cell_from_pgn('b5').piece.is_supported())
# print(b.get_cell_from_pgn('g2').piece.is_supported())