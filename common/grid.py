from dataclasses import dataclass
from typing import Iterator

from common.position import Position


@dataclass
class GridBase[T]:
    grid: list[list[T]]

    def __getitem__(self, key: Position) -> T:
        return self.grid[key.row][key.col]

    def __contains__(self, position: Position) -> bool:
        return (0 <= position.row < self.height) and (0 <= position.col < self.width)

    def __iter__(self) -> Iterator[tuple[Position, T]]:
        for row_idx, row in enumerate(self.grid):
            for col_idx, value in enumerate(row):
                yield Position(row_idx, col_idx), value

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)
