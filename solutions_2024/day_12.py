from dataclasses import dataclass
from collections import deque
from typing import TextIO

from common.position import Position
from common.solution import SolutionBase
from common.grid import GridBase
from common.direction import Direction


@dataclass
class Region:
    id: str
    positions: set[Position]

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    @property
    def discounted_price(self) -> int:
        return self.area * self.num_sides

    @property
    def area(self) -> int:
        return len(self.positions)

    @property
    def perimeter(self) -> int:
        total = 0
        for position in self.positions:
            for direction in Direction:
                offset_position = position.with_offset(direction.offset)
                if offset_position not in self.positions:
                    total += 1
        return total

    @property
    def num_sides(self) -> int:
        total = 0
        for position in self.positions:
            total += self.num_corners(position)
        return total

    def num_corners(self, position: Position) -> int:
        total = 0
        for direction in Direction:
            offset_position = position.with_offset(direction.offset)

            clockwise_direction = direction.clockwise_direction
            clockwise_offset_position = position.with_offset(clockwise_direction.offset)

            diag_offset_position = offset_position.with_offset(
                clockwise_direction.offset
            )

            if (
                # Inside corner
                offset_position in self.positions
                and clockwise_offset_position in self.positions
                and diag_offset_position not in self.positions
            ) or (
                # Outside corner
                offset_position not in self.positions
                and clockwise_offset_position not in self.positions
            ):
                total += 1

        return total


@dataclass
class GardenMap(GridBase[str]):
    @property
    def regions(self) -> list[Region]:
        regions: list[Region] = []
        visited: set[Position] = set()

        for position, _ in self:
            if position in visited:
                continue

            region = self._visit_region(position)
            regions.append(region)
            visited.update(region.positions)

        return regions

    def _visit_region(self, position: Position) -> Region:
        region_id = self[position]
        region = Region(region_id, set())

        visited: set[Position] = set()
        frontier: deque[Position] = deque([position])

        while frontier:
            current_position = frontier.popleft()
            if self[current_position] != region_id or current_position in visited:
                continue

            region.positions.add(current_position)
            visited.add(current_position)

            for direction in Direction:
                offset_position = current_position.with_offset(direction.offset)
                if offset_position in self:
                    frontier.append(offset_position)

        return region


TParsed = GardenMap


class Solution(SolutionBase[TParsed], year=2024, day=12):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        grid = [[char for char in line.strip()] for line in infile]
        return GardenMap(grid)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return sum(region.price for region in parsed_input.regions)

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        return sum(region.discounted_price for region in parsed_input.regions)
