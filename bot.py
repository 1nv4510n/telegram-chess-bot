import asyncio

from bot import __main__

# from bot.chess.board import Board
# from bot.chess.draw import draw_board
# from bot.chess.enums import Colors

asyncio.run(__main__.main())

# from bot.chess import Board
# from bot.chess.enums import Colors, PieceNames

# b = Board()
# b.add_pieces()

# print(b.get_cell_from_pgn('d8').is_attacked(Colors.BLACK))