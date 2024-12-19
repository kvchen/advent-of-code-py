from dataclasses import dataclass
from functools import cache
from typing import TextIO

from common.solution import SolutionBase


@dataclass(frozen=True)
class Onsen:
    patterns: tuple[str, ...]
    designs: tuple[str, ...]

    def possible_designs(self) -> list[str]:
        return [design for design in self.designs if self.is_design_possible(design)]

    @cache
    def is_design_possible(self, design: str) -> bool:
        if design == "":
            return True

        return any(
            self.is_design_possible(design[len(pattern) :])
            for pattern in self.patterns
            if design.startswith(pattern)
        )

    @cache
    def design_combinations(self, design: str) -> int:
        if design == "":
            return 1

        return sum(
            self.design_combinations(design[len(pattern) :])
            for pattern in self.patterns
            if design.startswith(pattern)
        )


TParsed = Onsen


class Solution(SolutionBase[TParsed], year=2024, day=19):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        it = iter(infile)
        patterns = tuple(next(it).strip().split(", "))

        next(it)

        designs: tuple[str, ...] = tuple(line.strip() for line in it)
        return Onsen(patterns, designs)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return len(
            [
                design
                for design in parsed_input.designs
                if parsed_input.is_design_possible(design)
            ]
        )

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        return sum(
            parsed_input.design_combinations(design) for design in parsed_input.designs
        )
