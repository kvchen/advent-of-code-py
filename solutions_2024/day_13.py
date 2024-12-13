import numpy as np
import re

from dataclasses import dataclass
from typing import TextIO
from itertools import islice

from common.solution import SolutionBase

np.set_printoptions(suppress=True, precision=100)


@dataclass
class ClawMachine:
    a: np.ndarray
    b: np.ndarray
    prize: np.ndarray

    def cheapest_cost(self) -> int:
        if (solution := self._solve()) is None:
            return 0

        return int(solution @ np.array([3, 1]))

    def _solve(self) -> np.ndarray | None:
        a = self.a[0]
        b = self.b[0]
        c = self.a[1]
        d = self.b[1]

        adj_matrix = np.array([[d, -b], [-c, a]])
        det = a * d - b * c

        A_inv_b_det = adj_matrix @ self.prize

        # Divide out the determinant later on to avoid precision issues

        if np.any(A_inv_b_det % det):  # type: ignore
            return None

        return (A_inv_b_det / det).round()


TParsed = list[ClawMachine]


class Solution(SolutionBase[TParsed], year=2024, day=13):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        parsed: TParsed = []

        it = iter(infile)
        while chunk := tuple(islice(it, 4)):
            button_a_match = re.match(
                r"^Button A: X\+(\d+), Y\+(\d+)$", chunk[0].strip()
            )
            button_b_match = re.match(
                r"^Button B: X\+(\d+), Y\+(\d+)$", chunk[1].strip()
            )
            prize_match = re.match(r"^Prize: X=(\d+), Y=(\d+)$", chunk[2].strip())

            assert button_a_match
            assert button_b_match
            assert prize_match

            cm = ClawMachine(
                a=np.array([int(x) for x in button_a_match.groups()]),
                b=np.array([int(x) for x in button_b_match.groups()]),
                prize=np.array([int(x) for x in prize_match.groups()]),
            )
            parsed.append(cm)

        return parsed

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return sum(cm.cheapest_cost() for cm in parsed_input)

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        offset = 10000000000000
        adjusted_cms = [
            ClawMachine(cm.a, cm.b, cm.prize + offset) for cm in parsed_input
        ]
        return sum(cm.cheapest_cost() for cm in adjusted_cms)
