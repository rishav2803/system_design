from typing import List
from snake_ladder.cell import Cell, LadderCell, NormalCell, SnakeCell


class Board:

    def __init__(self, board_size, snake_pos: dict, ladder_pos: dict):
        self.board_size = board_size
        self.snake_pos = snake_pos
        self.ladder_pos = ladder_pos
        self.board: List[Cell] = self.build_board()

    def build_board(self):
        board: List[Cell] = []
        seen_cells = set()

        for start, end in self.snake_pos.items():
            snake_cell = SnakeCell(tail_pos=end)
            board[start] = snake_cell
            seen_cells.add(start)

        for start, end in self.ladder_pos.items():
            ladder_cell = LadderCell(tail_pos=end)
            board[start] = ladder_cell
            seen_cells.add(start)

        for i in range(self.board_size):
            if i not in seen_cells:
                board[i] = NormalCell()

        return board
