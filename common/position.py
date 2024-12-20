from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Self, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def with_offset(self, offset: tuple[int, int]) -> Position:
        return Position(row=self.row + offset[0], col=self.col + offset[1])

    @classmethod
    def from_ndarray(cls, arr: np.ndarray) -> Self:
        return cls(row=int(arr[0]), col=int(arr[1]))

    def positions_within(
        self, euclidean_distance: int
    ) -> Iterator[tuple[Position, int]]:
        for row_offset in range(-euclidean_distance, euclidean_distance + 1):
            col_distance = euclidean_distance - abs(row_offset)
            for col_offset in range(-col_distance, col_distance + 1):
                distance = abs(row_offset) + abs(col_offset)
                if row_offset == 0 and col_offset == 0:
                    continue

                yield self.with_offset((row_offset, col_offset)), distance
