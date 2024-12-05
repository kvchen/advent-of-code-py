import re
from dataclasses import dataclass
from typing import TextIO, Protocol, Self, Iterator


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


class InterpreterBase(Protocol):
    def handle(self, instruction: InstructionBase) -> None: ...

    def run(self, infile: TextIO) -> None:
        for instruction in self._instructions(infile):
            self.handle(instruction)

    def _instructions(self, infile: TextIO) -> Iterator[InstructionBase]:
        for line in infile:
            for match in re.finditer(self._tokenizer_pattern(), line):
                yield self._instruction_from_match(match)

    def _tokenizer_pattern(self) -> str:
        return "|".join(
            f"(?P<{instruction_cls.__name__}>{instruction_cls.pattern()})"
            for instruction_cls in InstructionBase.__subclasses__()
        )

    def _instruction_from_match(self, match: re.Match[str]) -> InstructionBase:
        for instruction_cls in InstructionBase.__subclasses__():
            if match.group(instruction_cls.__name__):
                return instruction_cls.from_match(match)

        raise Exception(f"Unknown instruction: {match}")
