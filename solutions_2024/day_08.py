from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from typing import TextIO

from common.solution import SolutionBase


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def offset(self, other: "Position") -> tuple[int, int]:
        return self.row - other.row, self.col - other.col

    def with_offset(self, offset: tuple[int, int]) -> "Position":
        return Position(self.row + offset[0], self.col + offset[1])


@dataclass
class Map:
    width: int
    height: int
    antennas: dict[str, set[Position]] = field(default_factory=lambda: defaultdict(set))

    def in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self.height and 0 <= position.col < self.width


TParsed = Map


class Solution(SolutionBase[TParsed], year=2024, day=8):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        antennas: dict[str, set[Position]] = defaultdict(set)
        for row, line in enumerate(infile):
            for col, char in enumerate(line.strip()):
                if char not in {".", "#"}:
                    position = Position(row, col)
                    antennas[char].add(position)

        map = Map(width=col + 1, height=row + 1, antennas=antennas)  # type: ignore
        return map

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        locations: set[Position] = set()
        for positions in parsed_input.antennas.values():
            for p1, p2 in combinations(positions, 2):
                offset = p1.offset(p2)
                an1 = p1.with_offset(offset)
                an2 = p2.with_offset((-offset[0], -offset[1]))

                if parsed_input.in_bounds(an1):
                    locations.add(an1)
                if parsed_input.in_bounds(an2):
                    locations.add(an2)

        return len(locations)

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        locations: set[Position] = set()
        for positions in parsed_input.antennas.values():
            for p1, p2 in combinations(positions, 2):
                offset = p1.offset(p2)

                an1 = p1
                while parsed_input.in_bounds(an1):
                    locations.add(an1)
                    an1 = an1.with_offset(offset)

                neg_offset = (-offset[0], -offset[1])
                an2 = p2
                while parsed_input.in_bounds(an2):
                    locations.add(an2)
                    an2 = an2.with_offset(neg_offset)

        return len(locations)
