from dataclasses import dataclass
from typing import Callable, TextIO
from operator import add, mul

from common.solution import SolutionBase


def concat(x: int, y: int) -> int:
    return int(str(x) + str(y))


Operation = Callable[[int, int], int]


@dataclass
class Calibration:
    test_value: int
    values: list[int]

    def can_match(self, ops: list[Operation]) -> bool:
        return self._can_match_impl(ops, self.values[0], value_idx=1)

    def _can_match_impl(self, ops: list[Operation], total: int, value_idx: int) -> bool:
        if value_idx == len(self.values):
            return total == self.test_value

        value = self.values[value_idx]
        return any(
            self._can_match_impl(ops, op(total, value), value_idx + 1) for op in ops
        )


TParsed = list[Calibration]


class Solution(SolutionBase[TParsed], year=2024, day=7):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        calibrations: TParsed = []
        for line in infile:
            test_value, right = line.strip().split(":")
            values = right.strip().split()
            calibration = Calibration(
                test_value=int(test_value), values=[int(v) for v in values]
            )
            calibrations.append(calibration)

        return calibrations

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        total = 0
        for calibration in parsed_input:
            if calibration.can_match([add, mul]):
                total += calibration.test_value
        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        for calibration in parsed_input:
            if calibration.can_match([add, mul, concat]):
                total += calibration.test_value
        return total
