from dataclasses import dataclass
from typing import Iterator, TextIO

from common.direction import Direction
from common.solution import SolutionBase
from common.position import Position


@dataclass
class TopographicMap:
    height_map: list[list[int]]

    @property
    def width(self) -> int:
        return len(self.height_map[0])

    @property
    def height(self) -> int:
        return len(self.height_map)

    def in_bounds(self, position: Position) -> bool:
        return (0 <= position.row < self.height) and (0 <= position.col < self.width)

    def height_at(self, position: Position) -> int:
        return self.height_map[position.row][position.col]

    @property
    def trailheads(self) -> Iterator[Position]:
        for row_idx, row in enumerate(self.height_map):
            for col_idx, height in enumerate(row):
                if height == 0:
                    yield Position(row_idx, col_idx)

    def reachable_paths(self, position: Position) -> list[list[Position]]:
        height = self.height_at(position)
        if height == 9:
            return [[position]]

        paths: list[list[Position]] = []
        for direction in Direction:
            next_position = position.with_offset(direction.offset)
            if not self.in_bounds(next_position):
                continue

            if self.height_at(next_position) == (height + 1):
                paths.extend(
                    [position] + path for path in self.reachable_paths(next_position)
                )

        return paths


TParsed = TopographicMap


class Solution(SolutionBase[TParsed], year=2024, day=10):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        height_map: list[list[int]] = []
        for line in infile:
            row_heights = [int(c) for c in line.strip()]
            height_map.append(row_heights)

        return TopographicMap(height_map)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        total = 0
        for trailhead_position in parsed_input.trailheads:
            peaks: set[Position] = set()
            for path in parsed_input.reachable_paths(trailhead_position):
                peaks.add(path[-1])
            total += len(peaks)
        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        for trailhead_position in parsed_input.trailheads:
            total += len(parsed_input.reachable_paths(trailhead_position))
        return total
