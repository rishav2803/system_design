from abc import ABC, abstractmethod
from typing import Optional


class Cell(ABC):
    @abstractmethod
    def jump(self) -> Optional[int]:
        pass


class NormalCell(Cell):
    def jump(self):
        return None


class SnakeCell(Cell):
    # store some extra information like
    # this particular snake cell starts from where and ends where??
    def __init__(self, tail_pos: int):
        self.tail_pos = tail_pos

    # snake cell jumps downwards
    def jump(self):
        return -self.tail_pos


class LadderCell(Cell):
    def __init__(self, tail_pos: int):
        self.tail_pos = tail_pos

    # snake cell jumps upwards
    def jump(self):
        return self.tail_pos
