from typing import TextIO

from common.solution import SolutionBase


TParsed = list[int]


class Solution(SolutionBase[TParsed], year=2024, day=2):
    @staticmethod
    def parse_input(infile: TextIO) -> TParsed:
        return []

    @staticmethod
    def part_01(parsed_input: TParsed) -> int:
        return 0

    @staticmethod
    def part_02(parsed_input: TParsed) -> int:
        return 0
