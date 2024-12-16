from __future__ import annotations

from dataclasses import dataclass
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def with_offset(self, offset: tuple[int, int]) -> Self:
        return Position(row=self.row + offset[0], col=self.col + offset[1])

    @classmethod
    def from_ndarray(cls, arr: np.ndarray) -> Self:
        return cls(row=int(arr[0]), col=int(arr[1]))
