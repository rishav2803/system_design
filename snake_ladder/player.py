from snake_ladder.board import Board
from snake_ladder.dice import Dice
import time


class Player:

    def __init__(self, name: str, dice: Dice, board: Board) -> None:
        self.name = name
        self.postion = 1
        self.dice = dice
        self.board = board

    def play(self):
        print(f"Player {self.name} rolls the dice!!!")
        time.sleep(4)

        number = self.dice.roll()
        print(f"Player {self.name} rolled number {number}")

        new_pos = self.postion + number

        if new_pos > self.board.board_size:
            print(f"Player {self.name} went out of the board current turn is invalid")

        self.postion += number

        valid_jump = self.board.board[self.postion].jump()

        self.postion += 0 if not valid_jump else valid_jump
