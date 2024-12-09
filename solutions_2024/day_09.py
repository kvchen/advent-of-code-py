from copy import deepcopy
from dataclasses import dataclass
from typing import TextIO

from common.solution import SolutionBase


@dataclass
class Chunk:
    file_id: int
    length: int

    def __str__(self) -> str:
        # return f"[{self.file_id}:{self.length}]"
        return ("[.]" if self.is_free_space else f"[{self.file_id}]") * self.length

    @property
    def is_free_space(self) -> bool:
        return self.file_id == -1


@dataclass
class DiskMap:
    chunks: list[Chunk]

    def __str__(self) -> str:
        return ''.join(str(chunk) for chunk in self.chunks)

    def compress_blocks(self) -> "DiskMap":
        compressed_map = deepcopy(self)

        idx = 0
        while idx < len(compressed_map.chunks):
            chunk = compressed_map.chunks[idx]
            if chunk.is_free_space:
                while (last_chunk := compressed_map.chunks.pop()).is_free_space:
                    pass

                remaining_chunk = compressed_map._move_chunk(idx, last_chunk)
                if remaining_chunk:
                    compressed_map.chunks.append(remaining_chunk)

            idx += 1

        return compressed_map

    def compress_files(self) -> "DiskMap":
        compressed_map = deepcopy(self)        

        idx = len(compressed_map.chunks) - 1
        while idx > 0:
            chunk = compressed_map.chunks[idx]
            if not chunk.is_free_space:
                space_idx = compressed_map._find_free_space(
                    chunk.length, before_idx=idx
                )
                if space_idx >= 0:
                    compressed_map.chunks[idx] = Chunk(-1, chunk.length)
                    remaining_chunk = compressed_map._move_chunk(space_idx, chunk)
                    assert not remaining_chunk
                    idx += 1
            idx -= 1

        return compressed_map

    def checksum(self) -> int:
        total = 0
        offset = 0

        for chunk in self.chunks:
            if not chunk.is_free_space:
                for idx in range(chunk.length):
                    total += chunk.file_id * (offset + idx)
            offset += chunk.length
        return total

    def _find_free_space(self, length: int, before_idx: int) -> int:
        for idx in range(before_idx):
            chunk = self.chunks[idx]
            if chunk.is_free_space and chunk.length >= length:
                return idx
        return -1

    def _move_chunk(self, space_idx: int, chunk: Chunk) -> Chunk | None:
        space_chunk = self.chunks.pop(space_idx)

        if space_chunk.length == chunk.length:
            self.chunks.insert(space_idx, chunk)
        elif space_chunk.length > chunk.length:
            self.chunks.insert(space_idx, chunk)
            self.chunks.insert(
                space_idx + 1, Chunk(-1, space_chunk.length - chunk.length)
            )
        elif space_chunk.length < chunk.length:
            self.chunks.insert(space_idx, Chunk(chunk.file_id, space_chunk.length))
            return Chunk(chunk.file_id, chunk.length - space_chunk.length)


TParsed = DiskMap


class Solution(SolutionBase[TParsed], year=2024, day=9):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        chunks: list[Chunk] = []

        file_id = 0
        is_free_space = False

        for char in infile.read().strip():
            chunk_length = int(char)
            if is_free_space:
                chunk = Chunk(-1, chunk_length)
            else:
                chunk = Chunk(file_id, chunk_length)
                file_id += 1

            chunks.append(chunk)
            is_free_space = not is_free_space

        return DiskMap(chunks)

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        return parsed_input.compress_blocks().checksum()

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        return parsed_input.compress_files().checksum()
