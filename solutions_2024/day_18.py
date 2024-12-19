from dataclasses import dataclass
from typing import TextIO

import networkx as nx

from common.direction import Direction
from common.position import Position
from common.solution import SolutionBase


@dataclass
class Map:
    byte_positions: list[Position]
    width: int = 71
    height: int = 71

    def graph(self, steps: int) -> nx.DiGraph:
        byte_positions = self.byte_positions[:steps]
        g = nx.DiGraph()

        # Pass 1: Populate nodes

        for row in range(self.height):
            for col in range(self.width):
                pos = Position(row, col)
                if pos not in byte_positions:
                    g.add_node(pos)

        # Pass 2: Populate edges

        for pos in g.nodes:
            for direction in Direction:
                offset_pos = pos.with_offset(direction.offset)
                if offset_pos in g.nodes:
                    g.add_edge(pos, offset_pos)

        return g


TParsed = Map


class Solution(SolutionBase[TParsed], year=2024, day=18):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        byte_positions = list(
            Position(*map(int, line.strip().split(","))) for line in infile
        )
        return Map(byte_positions)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return nx.shortest_path_length(
            parsed_input.graph(steps=1024),
            Position(0, 0),
            Position(parsed_input.height - 1, parsed_input.width - 1),
        )

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        # TODO(@kvchen): Manually bin'searched this, add actual binary search later
        for steps in range(2954, 2964, 1):
            print(steps)
            nx.shortest_path_length(
                parsed_input.graph(steps=steps),
                Position(0, 0),
                Position(parsed_input.height - 1, parsed_input.width - 1),
            )

        return 0
