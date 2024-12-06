from collections import defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from typing import Mapping, Self, TextIO

from common.solution import SolutionBase


@dataclass
class PageRules:
    rules: Mapping[int, set[int]]

    def page_comparator(self, a: int, b: int) -> int:
        if a == b:
            return 0
        elif b in self.rules[a]:
            return -1
        else:
            return 1


@dataclass
class Update:
    pages: list[int]

    def to_sorted(self, rules: PageRules) -> Self:
        sorted_pages = sorted(self.pages, key=cmp_to_key(rules.page_comparator))
        return Update(pages=sorted_pages)

    def midpoint_value(self) -> int:
        mid_idx = len(self.pages) // 2
        return self.pages[mid_idx]


TParsed = tuple[PageRules, list[Update]]


class Solution(SolutionBase[TParsed], year=2024, day=5):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        rules: defaultdict[int, set[int]] = defaultdict(set)
        updates: list[Update] = []

        infile_iter = iter(infile.readlines())
        for line in infile_iter:
            if not line.strip():
                break

            x, y = line.strip().split("|")
            rules[int(x)].add(int(y))

        for line in infile_iter:
            pages = line.strip().split(",")
            updates.append(Update(pages=[int(p) for p in pages]))

        return PageRules(rules=rules), updates

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        total = 0
        page_dependencies, updates = parsed_input
        for update in updates:
            if update == update.to_sorted(page_dependencies):
                total += update.midpoint_value()

        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        page_dependencies, updates = parsed_input
        for update in updates:
            sorted_update = update.to_sorted(page_dependencies)
            if update != update.to_sorted(page_dependencies):
                total += sorted_update.midpoint_value()

        return total
