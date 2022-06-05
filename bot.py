import asyncio
from time import time
from uuid import uuid4
from bot import __main__
from bot import chess
from bot.chess.enums import Colors, PieceIcons, PieceNames
from bot.chess.player import Player
asyncio.run(__main__.main())

# async def main():
#     game_id = uuid4()
#     player1 = Player(123123, game_id, Colors.WHITE)
#     player2 = Player(12312553, game_id, Colors.BLACK)

#     game = chess.Game(game_id, player1, player2)
    
#     print(await game.highlight_moves(player1, 'h2'))

# timer = time()
# asyncio.run(main())
# print(time() - timer)