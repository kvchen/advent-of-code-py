from typing import TextIO

from common.solution import SolutionBase


TParsed = list[list[int]]


class Solution(SolutionBase[TParsed], year=2024, day=2):
    @classmethod
    def parse_input(cls, infile: TextIO) -> TParsed:
        reports: TParsed = []
        for line in infile:
            report = [int(level) for level in line.split()]
            reports.append(report)

        return reports

    @classmethod
    def part_01(cls, parsed_input: TParsed) -> int:
        num_safe_reports = 0
        for report in parsed_input:
            if cls.is_safe(report):
                num_safe_reports += 1

        return num_safe_reports

    @classmethod
    def part_02(cls, parsed_input: TParsed) -> int:
        num_safe_reports = 0
        for report in parsed_input:
            if cls.is_safe_lenient(report):
                num_safe_reports += 1

        return num_safe_reports

    @classmethod
    def is_safe(cls, report: list[int]) -> bool:
        if report[0] == report[1]:
            return False

        is_safe = True
        is_increasing = report[1] > report[0]

        for first, second in zip(report[:-1], report[1:]):
            if is_increasing:
                if second <= first or second > first + 3:
                    is_safe = False
                    break
            else:
                if second >= first or second < first - 3:
                    is_safe = False
                    break

        return is_safe

    @classmethod
    def is_safe_lenient(cls, report: list[int]) -> bool:
        if cls.is_safe(report):
            return True

        # TODO(@keffcat): Brute force for now.
        # This can be done more efficiently by comparing against adjacent values.
        # Always attempt to greedily remove problematic values.

        for idx in range(len(report)):
            damped_report = report[:idx] + report[idx + 1 :]
            if cls.is_safe(damped_report):
                return True

        return False
