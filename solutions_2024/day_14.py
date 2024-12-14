from math import prod
import re
import numpy as np

from collections import Counter
from dataclasses import dataclass
from typing import Self, TextIO

from common.solution import SolutionBase


@dataclass
class Robot:
    position: np.ndarray
    velocity: np.ndarray

    def simulate(self, steps: int) -> Self:
        return Robot(self.position + self.velocity * steps, self.velocity)


@dataclass
class Bathroom:
    size: np.ndarray
    robots: list[Robot]

    def __str__(self) -> str:
        grid = np.zeros(self.size)
        for robot in self.robots:
            grid[*robot.position] += 1

        out = ""
        for row in grid.T:
            out += "".join("." if col == 0 else str(int(col)) for col in row) + "\n"

        return out

    def simulate(self, steps: int) -> Self:
        robots = [robot.simulate(steps) for robot in self.robots]
        for robot in robots:
            robot.position = robot.position % self.size
        return Bathroom(self.size, robots)

    def to_grid(self) -> np.ndarray:
        grid = np.zeros(self.size)
        for robot in self.robots:
            grid[*robot.position] += 1
        return grid

    def safest_area(self) -> int:
        counts: Counter[tuple[bool, bool]] = Counter()
        midpoint = self.size // 2

        for robot in self.robots:
            if np.any(robot.position == midpoint):  # type: ignore
                continue

            counts[tuple(robot.position < midpoint)] += 1  # type: ignore

        return prod(counts.values())


TParsed = Bathroom


class Solution(SolutionBase[TParsed], year=2024, day=14):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        robots: list[Robot] = []

        for line in infile:
            match = re.match(r"^p=(.*),(.*) v=(.*),(.*)$", line.strip())
            assert match

            groups = match.groups()
            position = np.array([int(groups[0]), int(groups[1])])
            velocity = np.array([int(groups[2]), int(groups[3])])

            robots.append(Robot(position, velocity))

        # size = np.array([11, 7])
        size = np.array([101, 103])
        return Bathroom(size, robots)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        simulated = parsed_input.simulate(steps=100)
        return simulated.safest_area()

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        i = 0
        while True:
            i += 1
            simulated = parsed_input.simulate(steps=i)
            if not np.any(simulated.to_grid() > 1):  # type: ignore
                print(simulated)
                return i
