from collections import Counter
from dataclasses import dataclass
from typing import Self, TextIO

from common.solution import SolutionBase


@dataclass
class StoneLine:
    value_counts: Counter[int]

    def blink(self) -> Self:
        next_counts: Counter[int] = Counter()
        for value, count in self.value_counts.items():
            if value == 0:
                next_counts[1] += count
                continue

            value_str = str(value)
            if len(value_str) % 2 == 0:
                midpoint_idx = len(value_str) // 2
                next_counts[int(value_str[:midpoint_idx])] += count
                next_counts[int(value_str[midpoint_idx:])] += count
                continue

            next_counts[value * 2024] += count

        return StoneLine(next_counts)

    def num_stones(self) -> int:
        return self.value_counts.total()


TParsed = StoneLine


class Solution(SolutionBase[TParsed], year=2024, day=11):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        return StoneLine(Counter(int(x) for x in infile.read().strip().split()))

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        for _ in range(25):
            parsed_input = parsed_input.blink()
        return parsed_input.num_stones()

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        for _ in range(75):
            parsed_input = parsed_input.blink()
        return parsed_input.num_stones()
