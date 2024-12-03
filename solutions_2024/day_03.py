from typing import TextIO

from common.interpreter import (
    InterpreterBase,
    DoInstruction,
    DontInstruction,
    MulInstruction,
    InstructionBase
)
from common.solution import SolutionBase


TParsed = TextIO


class Part01Interpreter(InterpreterBase):
    def __init__(self):
        self.total = 0
    
    def handle(self, instruction: InstructionBase):
        match instruction:
            case MulInstruction(x, y):
                self.total += x * y
            case _:
                pass


class Part02Interpreter(InterpreterBase):
    def __init__(self):
        self.total = 0
        self.is_mul_enabled = True
    
    def handle(self, instruction: InstructionBase):
        match instruction:
            case MulInstruction(x, y):
                if self.is_mul_enabled:
                    self.total += x * y
            case DoInstruction():
                self.is_mul_enabled = True
            case DontInstruction():
                self.is_mul_enabled = False
            case _:
                pass



class Solution(SolutionBase[TParsed], year=2024, day=3):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        return infile

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        interpreter = Part01Interpreter()
        interpreter.run(parsed_input)

        return interpreter.total

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        interpreter = Part02Interpreter()
        interpreter.run(parsed_input)

        return interpreter.total
