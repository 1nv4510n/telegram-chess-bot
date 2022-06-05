from typing import List, Union
from PIL import Image, ImageDraw
from .enums import BoardParam
from .board import Board, Cell
 
def get_offsets(cells: List[List[Cell]], turn_over: bool) -> List[List[Union[str, int]]]:
    offsets = []
    if not turn_over:
        for i in range(len(cells)):
            row = cells[i]
            for j in range(len(row)):
                target_cell = row[j]
                if target_cell.piece:
                    offsets.append(
                        [
                            f'chess\\pieces\\{target_cell.piece.logo}',
                            (target_cell.x * BoardParam.CELL_SIZE.value + BoardParam.OFFSET_X.value, target_cell.y * BoardParam.CELL_SIZE.value + BoardParam.OFFSET_Y.value)
                        ]
                    )
    else:
        for i in range(len(cells) - 1, -1, -1):
            row = cells[i]
            for j in range(len(row) -1, -1, -1):
                target_cell = row[j]
                if target_cell.piece:
                    offsets.append(
                        [
                            f'chess\\pieces\\{target_cell.piece.logo}', 
                        ((BoardParam.BOARD_SIZE.value - 1 - target_cell.x) * BoardParam.CELL_SIZE.value + BoardParam.ROTATE_OFFSET_X.value, 
                        (BoardParam.BOARD_SIZE.value - 1 - target_cell.y) * BoardParam.CELL_SIZE.value + BoardParam.ROTATE_OFFSET_Y.value)
                        ]
                    )
    return offsets
    
def draw_pure_board() -> None:
    cell_size = BoardParam.CELL_SIZE.value
    new_color = (201, 146, 92)
    new_image = Image.new("RGB", (8 * cell_size, 8 * cell_size), new_color)
    x = cell_size * 8
    y = x
    draw = ImageDraw.Draw(new_image)
    for i in range(0, x, cell_size):
        if i % (cell_size * 2) == 0:
            for j in range(0, y, cell_size):
                if j % (cell_size * 2) == 0:
                    draw.rectangle([i, j, i + cell_size - 1, j + cell_size - 1], fill = (235, 213, 180), width=0)
        else:
            for j in range(cell_size, y, cell_size):
                if j % (cell_size * 2) != 0:
                    draw.rectangle([i, j, i + cell_size - 1, j + cell_size - 1], fill = (235, 213, 180), width=0)

def draw_board(board: Board, turn_over: bool) -> None:
    pure_board = Image.open('chess\\pure_board.png', 'r')
    if turn_over:
        pure_board = pure_board.rotate(180)
    
    for piece in get_offsets(board.cells, turn_over):
        image = Image.open(piece[0], 'r')
        pure_board.paste(image, piece[1], image)               
    
    pure_board.save('res.png', "PNG")