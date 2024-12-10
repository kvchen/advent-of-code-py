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

    def num_paths_from(self, position: Position) -> int:
        height = self.height_at(position)
        if height == 9:
            return 1

        num_paths = 0
        for direction in Direction:
            next_position = position.with_offset(direction.offset)
            if self.in_bounds(next_position) and self.height_at(next_position) == (height + 1):
                num_paths += self.num_paths_from(next_position)
        return num_paths

    def reachable_peaks(self, position: Position) -> set[Position]:
        height = self.height_at(position)
        if height == 9:
            return {position}

        peaks: set[Position] = set()
        for direction in Direction:
            next_position = position.with_offset(direction.offset)
            if self.in_bounds(next_position) and self.height_at(next_position) == (height + 1):
                peaks = peaks.union(self.reachable_peaks(next_position))
        return peaks


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
            peaks = parsed_input.reachable_peaks(trailhead_position)
            total += len(peaks)

        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        for trailhead_position in parsed_input.trailheads:
            total += parsed_input.num_paths_from(trailhead_position)

        return total
