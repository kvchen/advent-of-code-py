# from dataclasses import dataclass
from typing import TextIO

from common.solution import SolutionBase


TParsed = list[int]


class Solution(SolutionBase[TParsed], year=2020, day=1):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        return []

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return 0

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        return 0
