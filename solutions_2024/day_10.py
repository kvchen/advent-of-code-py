from dataclasses import dataclass
from typing import Iterator, TextIO

from common.direction import Direction
from common.grid import GridBase
from common.solution import SolutionBase
from common.position import Position


@dataclass
class TopographicMap(GridBase[int]):
    @property
    def trailheads(self) -> Iterator[Position]:
        for position, value in iter(self):
            if value == 0:
                yield position

    def reachable_paths(self, position: Position) -> list[list[Position]]:
        height = self[position]
        if height == 9:
            return [[position]]

        paths: list[list[Position]] = []
        for direction in Direction:
            next_position = position.with_offset(direction.offset)
            if next_position not in self:
                continue

            if self[next_position] == (height + 1):
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
