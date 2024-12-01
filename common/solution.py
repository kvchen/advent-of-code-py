from enum import StrEnum
from typing import Protocol, TextIO, ClassVar


class BaseSolution[TParsed](Protocol):
    _registry: "ClassVar[dict[tuple[int, int], BaseSolution[object]]]" = {}

    class Part(StrEnum):
        ONE = "one"
        TWO = "two"

    def __init_subclass__(cls, year: int, day: int):
        cls._registry[(year, day)] = cls  # type: ignore

    @classmethod
    def get_solution(cls, year: int, day: int) -> "BaseSolution[object]":
        return cls._registry[(year, day)]

    @staticmethod
    def parse_input(infile: TextIO) -> TParsed: ...

    @staticmethod
    def part_01(parsed_input: TParsed) -> int: ...

    @staticmethod
    def part_02(parsed_input: TParsed) -> int: ...

    @classmethod
    def solve(cls, infile: TextIO, part: Part) -> int:
        parsed_input = cls.parse_input(infile)

        match part:
            case cls.Part.ONE:
                return cls.part_01(parsed_input)
            case cls.Part.TWO:
                return cls.part_02(parsed_input)
