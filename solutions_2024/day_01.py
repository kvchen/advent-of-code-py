from collections import Counter
from typing import TextIO

from common.solution import SolutionBase


TParsed = tuple[list[int], list[int]]


class Solution(SolutionBase[TParsed], year=2024, day=1):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        left: list[int] = []
        right: list[int] = []

        for line in infile:
            lvalue, rvalue = line.split()
            left.append(int(lvalue))
            right.append(int(rvalue))

        return left, right

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        left, right = parsed_input
        sorted_left = sorted(left)
        sorted_right = sorted(right)

        total = 0
        for lvalue, rvalue in zip(sorted_left, sorted_right):
            total += abs(rvalue - lvalue)

        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        left, right = parsed_input
        counter_right = Counter(right)

        total = 0
        for lvalue in left:
            if lvalue not in counter_right:
                continue

            total += lvalue * counter_right[lvalue]

        return total
