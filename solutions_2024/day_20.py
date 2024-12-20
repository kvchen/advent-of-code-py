from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from typing import TextIO

import networkx as nx

from common.direction import Direction
from common.position import Position
from common.solution import SolutionBase


@dataclass(frozen=True)
class Racetrack:
    graph: nx.DiGraph
    start: Position
    end: Position

    @cached_property
    def dists_from_start(self) -> dict[Position, int]:
        return nx.shortest_path_length(self.graph, source=self.start)

    @cached_property
    def dists_to_end(self) -> dict[Position, int]:
        return nx.shortest_path_length(self.graph, target=self.end)

    def num_cheats(self, *, max_skipped_steps: int, threshold: int) -> int:
        normal_shortest_path_length = nx.shortest_path_length(
            self.graph,
            source=self.start,
            target=self.end,
        )
        threshold = normal_shortest_path_length - threshold
        counter: Counter[int] = Counter()

        for pos in self.graph.nodes():
            for neighbor_pos, neighbor_distance in pos.positions_within(
                max_skipped_steps
            ):
                if neighbor_pos not in self.graph.nodes():
                    continue

                dist = (
                    self.dists_from_start[pos]
                    + self.dists_to_end[neighbor_pos]
                    + neighbor_distance
                )
                if dist <= threshold:
                    counter[normal_shortest_path_length - dist] += 1

        return counter.total()


TParsed = Racetrack


class Solution(SolutionBase[TParsed], year=2024, day=20):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        start_position = None
        end_position = None

        g = nx.DiGraph()
        for row, line in enumerate(infile):
            for col, char in enumerate(line.strip()):
                if char == "#":
                    continue

                pos = Position(row, col)

                match char:
                    case "S":
                        start_position = pos
                    case "E":
                        end_position = pos

                g.add_node(pos)

        assert start_position is not None
        assert end_position is not None

        for pos in g.nodes():
            for direction in Direction:
                neighbor_pos = pos.with_offset(direction.offset)
                if neighbor_pos in g.nodes():
                    g.add_edge(pos, neighbor_pos)

        return Racetrack(nx.freeze(g), start_position, end_position)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return parsed_input.num_cheats(max_skipped_steps=2, threshold=100)

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        return parsed_input.num_cheats(max_skipped_steps=20, threshold=100)
