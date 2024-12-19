from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, TextIO

from common.solution import SolutionBase


class HaltException(Exception):
    pass


Program = list[int]


@dataclass
class Computer:
    a: int
    b: int
    c: int

    inst_ptr: int = 0
    outputs: list[int] = field(default_factory=list)

    # Instructions

    def adv(self, operand: int) -> int:
        self.a = self.a // (2 ** self._combo_operand(operand))
        return 2

    def bxl(self, operand: int) -> int:
        self.b = self.b ^ self._literal_operand(operand)
        return 2

    def bst(self, operand: int) -> int:
        self.b = self._combo_operand(operand) % 8
        return 2

    def jnz(self, operand: int) -> int:
        if self.a != 0:
            result = self._literal_operand(operand)
            self.inst_ptr = result
            return 0
        return 2

    def bxc(self, operand: int) -> int:
        self.b = self.b ^ self.c
        return 2

    def out(self, operand: int) -> int:
        self.outputs.append(self._combo_operand(operand) % 8)
        return 2

    def bdv(self, operand: int) -> int:
        self.b = self.a // (2 ** self._combo_operand(operand))
        return 2

    def cdv(self, operand: int) -> int:
        self.c = self.a // (2 ** self._combo_operand(operand))
        return 2

    # Instruction

    def run_program(self, program: Program) -> None:
        try:
            while True:
                instruction = self._read_instruction(program)
                operand = self._read_program_value(program, self.inst_ptr + 1)
                offset = instruction(operand)

                self.inst_ptr += offset

        except HaltException:
            return

    def _read_program_value(self, program: Program, offset: int) -> int:
        if 0 <= offset < len(program):
            return program[offset]

        raise HaltException()

    def _read_instruction(self, program: Program) -> Callable[[int], int]:
        match self._read_program_value(program, self.inst_ptr):
            case 0:
                return self.adv
            case 1:
                return self.bxl
            case 2:
                return self.bst
            case 3:
                return self.jnz
            case 4:
                return self.bxc
            case 5:
                return self.out
            case 6:
                return self.bdv
            case 7:
                return self.cdv
            case _:
                raise ValueError("Invalid opcode {}")

    def _literal_operand(self, operand: int) -> int:
        return operand

    def _combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Reserved operand {operand}")


TParsed = tuple[Computer, list[int]]


class Solution(SolutionBase[TParsed], year=2024, day=17):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        lines = infile.read().strip().splitlines()
        a = int(lines[0].split(": ")[1])
        b = int(lines[1].split(": ")[1])
        c = int(lines[2].split(": ")[1])
        program = list(map(int, lines[4].split(": ")[1].split(",")))

        return Computer(a, b, c), program

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> str:
        computer, program = parsed_input
        computer.run_program(program)

        return ",".join(map(str, computer.outputs))

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        # Program: 2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0

        # 2, 4: B = A % 8   << NOTE: Bottom 3 digits are thrown away! Can multiply A by 8 and brute force next value.
        # 1, 1: B = B XOR 1
        # 7, 5: C = A // (2 ** B)
        # 1, 5: B = B XOR 5
        # 4, 3: B = B ^ C
        # 5, 5: output B
        # 0, 3: A = A // 8
        # 3, 0: jump to 0

        computer, program = parsed_input

        a = 0
        for idx in range(len(program)):
            a *= 8
            while True:
                computer_copy = deepcopy(computer)
                computer_copy.a = a
                computer_copy.run_program(program)

                if computer_copy.outputs[-idx - 1 :] == program[-idx - 1 :]:
                    break

                a += 1

        return a
