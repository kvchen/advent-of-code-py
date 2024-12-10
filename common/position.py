from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def with_offset(self, offset: tuple[int, int]) -> Self:
        return Position(row=self.row + offset[0], col=self.col + offset[1])
