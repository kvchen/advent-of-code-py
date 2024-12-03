import re
from dataclasses import dataclass
from typing import TextIO, Protocol, Self

from common.solution import SolutionBase


class InstructionBase(Protocol):
    @staticmethod
    def pattern() -> str: ...

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self: ...


@dataclass
class MulInstruction(InstructionBase):
    x: int
    y: int

    @staticmethod
    def pattern() -> str:
        return r"mul\((?P<mul_x>\d+),(?P<mul_y>\d+)\)"

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self:
        x = int(match.group("mul_x"))
        y = int(match.group("mul_y"))
        return cls(x=x, y=y)


@dataclass
class DoInstruction(InstructionBase):
    @staticmethod
    def pattern() -> str:
        return r"do\(\)"

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self:
        return cls()


@dataclass
class DontInstruction(InstructionBase):
    @staticmethod
    def pattern() -> str:
        return r"don't\(\)"

    @classmethod
    def from_match(cls, match: re.Match[str]) -> Self:
        return cls()


Instruction = MulInstruction | DoInstruction | DontInstruction
InstructionTypes: list[type[Instruction]] = [
    MulInstruction,
    DoInstruction,
    DontInstruction,
]


TParsed = list[Instruction]


class Solution(SolutionBase[TParsed], year=2024, day=3):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        tokenizer_regex = "|".join(
            f"(?P<{instruction_cls.__name__}>{instruction_cls.pattern()})"
            for instruction_cls in InstructionTypes
        )

        parsed: TParsed = []
        for line in infile:
            for match in re.finditer(tokenizer_regex, line):
                parsed.append(cls.get_instruction(match))

        return parsed

    @classmethod
    def get_instruction(cls, match: re.Match[str]) -> Instruction:
        for instruction_cls in InstructionTypes:
            if match.group(instruction_cls.__name__):
                return instruction_cls.from_match(match)

        raise Exception(f"Unknown instruction: {match}")

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        total = 0
        for instruction in parsed_input:
            match instruction:
                case MulInstruction(x, y):
                    total += x * y
                case _:
                    pass

        return total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        total = 0
        is_mul_enabled = True

        for instruction in parsed_input:
            match instruction:
                case MulInstruction(x, y):
                    if is_mul_enabled:
                        total += x * y
                case DoInstruction():
                    is_mul_enabled = True
                case DontInstruction():
                    is_mul_enabled = False

        return total
