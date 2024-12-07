from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import Self, TextIO

from common.solution import SolutionBase


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    @property
    def clockwise_direction(self) -> Self:
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH

    @property
    def offset(self) -> tuple[int, int]:
        match self:
            case Direction.NORTH:
                return (-1, 0)
            case Direction.EAST:
                return (0, 1)
            case Direction.SOUTH:
                return (1, 0)
            case Direction.WEST:
                return (0, -1)


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def with_offset(self, offset: tuple[int, int]) -> Self:
        return Position(row=self.row + offset[0], col=self.col + offset[1])


@dataclass
class Map:
    obstructions: set[Position]
    width: int = 0
    height: int = 0

    def has_obstruction(self, position: Position) -> bool:
        return position in self.obstructions


@dataclass(frozen=True)
class Guard:
    position: Position
    direction: Direction = Direction.NORTH

    def move(self, map: Map) -> Self:
        new_position = self.position.with_offset(self.direction.offset)
        if map.has_obstruction(new_position):
            return Guard(
                position=self.position, direction=self.direction.clockwise_direction
            )

        return Guard(position=new_position, direction=self.direction)

    def in_bounds(self, map: Map) -> bool:
        return (0 <= self.position.row < map.height) and (
            0 <= self.position.col < map.width
        )


TParsed = tuple[Map, Guard]


class Solution(SolutionBase[TParsed], year=2024, day=6):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        map = Map(obstructions=set())
        guard = None

        for row_idx, line in enumerate(infile):
            for col_idx, char in enumerate(line):
                position = Position(row=row_idx, col=col_idx)
                match char:
                    case "#":
                        map.obstructions.add(position)
                    case "^":
                        guard = Guard(position=position)
                    case _:
                        pass

        map.width = col_idx + 1  # type: ignore
        map.height = row_idx + 1  # type: ignore

        assert guard is not None, "Guard not found in input map."
        return map, guard

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        map, guard = parsed_input
        positions: set[Position] = set()

        while guard.in_bounds(map):
            positions.add(guard.position)
            guard = guard.move(map)

        return len(positions)

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        # TODO(@kvchen): eh just brute force it for now

        map, guard = parsed_input
        total = 0

        for o_row in range(map.height):
            for o_col in range(map.width):
                obstruction_position = Position(row=o_row, col=o_col)
                if guard.position == obstruction_position:
                    continue

                map_with_obstruction = deepcopy(map)
                map_with_obstruction.obstructions.add(obstruction_position)

                test_guard = deepcopy(guard)
                previous_states: set[Guard] = set()

                caused_loop = False
                while test_guard.in_bounds(map_with_obstruction):
                    if test_guard in previous_states:
                        caused_loop = True
                        break

                    previous_states.add(test_guard)
                    test_guard = test_guard.move(map_with_obstruction)

                if caused_loop:
                    total += 1

        return total
