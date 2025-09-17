import random


class Dice:

    def __init__(self, n) -> None:
        self.n = n

    def roll(self):
        return random.randint(1, self.n)
