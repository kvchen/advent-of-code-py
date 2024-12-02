from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, TextIO, ClassVar


@dataclass(kw_only=True, frozen=True)
class RegistryKey:
    year: int
    day: int


class SolutionBase[TParsed](Protocol):
    _registry: "ClassVar[dict[RegistryKey, SolutionBase[object]]]" = {}

    class Part(StrEnum):
        ONE = "one"
        TWO = "two"

    def __init_subclass__(cls, year: int, day: int):
        registry_key = RegistryKey(year=year, day=day)
        assert (
            registry_key not in cls._registry
        ), f"A solution already exists for day {day}, year {year}"

        cls._registry[registry_key] = cls  # type: ignore

    @classmethod
    def get_solution(cls, year: int, day: int) -> "SolutionBase[object]":
        registry_key = RegistryKey(year=year, day=day)
        return cls._registry[registry_key]

    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed: ...

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int: ...

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int: ...

    @classmethod
    def solve(cls, infile: TextIO, part: Part) -> int:
        parsed_input = cls.parse_input(infile)

        match part:
            case cls.Part.ONE:
                return cls.part_01(parsed_input)
            case cls.Part.TWO:
                return cls.part_02(parsed_input)
