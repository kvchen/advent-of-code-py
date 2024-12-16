from enum import auto, Enum
from typing import Self


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
    def counterclockwise_direction(self) -> Self:
        match self:
            case Direction.NORTH:
                return Direction.WEST
            case Direction.EAST:
                return Direction.NORTH
            case Direction.SOUTH:
                return Direction.EAST
            case Direction.WEST:
                return Direction.SOUTH

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
