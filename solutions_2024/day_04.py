from dataclasses import dataclass
from typing import TextIO
from itertools import product

from common.solution import SolutionBase


TARGET_TEXT = "XMAS"
DIRECTIONS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


@dataclass
class SearchGrid:
    rows: list[list[str]]

    def letter(self, row: int, col: int) -> str:
        return self.rows[row][col]

    @property
    def width(self) -> int:
        return len(self.rows[0])

    @property
    def height(self) -> int:
        return len(self.rows)


@dataclass
class SearchState:
    row: int
    col: int
    text: str


TParsed = SearchGrid


class Solution(SolutionBase[TParsed], year=2024, day=4):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        return SearchGrid(rows=[[letter for letter in line.strip()] for line in infile])

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        total = 0
        for row, col in product(range(parsed_input.height), range(parsed_input.width)):
            for direction in DIRECTIONS:
                if cls.search(
                    parsed_input, SearchState(row=row, col=col, text=""), direction
                ):
                    total += 1
        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        for row, col in product(
            range(1, parsed_input.height - 1), range(1, parsed_input.width - 1)
        ):
            if parsed_input.letter(row, col) == "A":
                if cls.check_xmas(parsed_input, row, col):
                    total += 1
        return total

    @classmethod
    def check_xmas(cls, grid: TParsed, row: int, col: int) -> bool:
        diag_a = grid.letter(row - 1, col - 1) + grid.letter(row + 1, col + 1)
        diag_b = grid.letter(row - 1, col + 1) + grid.letter(row + 1, col - 1)
        matches = ("MS", "SM")

        return diag_a in matches and diag_b in matches

    @classmethod
    def search(
        cls, grid: TParsed, search_state: SearchState, direction: tuple[int, int]
    ) -> bool:
        if search_state.text == TARGET_TEXT:
            return True
        elif not TARGET_TEXT.startswith(search_state.text):
            return False
        elif search_state.row < 0 or search_state.row >= grid.height:
            return False
        elif search_state.col < 0 or search_state.col >= grid.width:
            return False

        next_letter = grid.letter(search_state.row, search_state.col)

        return cls.search(
            grid,
            SearchState(
                row=search_state.row + direction[0],
                col=search_state.col + direction[1],
                text=search_state.text + next_letter,
            ),
            direction,
        )
