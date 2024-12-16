from collections import deque
from dataclasses import dataclass
from typing import Iterator, Literal, TextIO

import networkx as nx
import numpy as np

from common.direction import Direction
from common.grid import GridBase
from common.position import Position
from common.solution import SolutionBase


@dataclass
class Reindeer:
    position: np.ndarray
    direction: Direction = Direction.EAST


@dataclass
class Map:
    graph: nx.DiGraph
    start: Position
    end: Position

    def shortest_path_length(self) -> int:
        return nx.shortest_path_length(
            self.graph, (self.start, Direction.EAST), "END", weight="weight"
        )

    def all_shortest_paths(
        self,
    ) -> Iterator[list[tuple[Position, Direction]]]:
        for path in nx.all_shortest_paths(
            self.graph, (self.start, Direction.EAST), "END", weight="weight"
        ):
            yield path[:-1]  # type: ignore


TParsed = Map


class Solution(SolutionBase[TParsed], year=2024, day=16):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        raw_grid = np.array([[c for c in row.strip()] for row in infile])

        spaces = np.transpose(np.where(raw_grid != "#"))
        start_pos = Position.from_ndarray(np.transpose(np.where(raw_grid == "S"))[0])
        end_pos = Position.from_ndarray(np.transpose(np.where(raw_grid == "E"))[0])

        graph = nx.DiGraph()

        # Pass 1: Populate nodes

        for space_pos in spaces:
            for direction in Direction:
                graph.add_node((Position.from_ndarray(space_pos), direction))

        # Pass 2: Populate edges

        for pos, direction in graph.nodes:
            offset_pos = pos.with_offset(direction.offset)
            if (offset_pos, direction) in graph.nodes:
                graph.add_edge(
                    (pos, direction),
                    (offset_pos, direction),
                    weight=1,
                )

            for rot_direction in (
                direction.clockwise_direction,
                direction.counterclockwise_direction,
            ):
                graph.add_edge((pos, direction), (pos, rot_direction), weight=1000)

        # We don't care what direction we're facing when we reach the end
        for direction in Direction:
            graph.add_edge((end_pos, direction), "END", weight=0)

        return Map(graph=graph, start=start_pos, end=end_pos)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return parsed_input.shortest_path_length()

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        seats = set()
        for path in parsed_input.all_shortest_paths():
            for pos, _ in path:
                seats.add(pos)
        return len(seats)
