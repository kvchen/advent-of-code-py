import click
from common.solution import BaseSolution
from typing import TextIO

from solutions_2024 import *


@click.command()
@click.option("--year", type=int, default=2024)
@click.option("--day", type=int, required=True)
@click.option("--part", type=click.Choice(list(BaseSolution.Part)), required=True)
@click.option("--input", type=click.File("r"), required=True)
def main(year: int, day: int, part: BaseSolution.Part, input: TextIO):
    solution = BaseSolution.get_solution(year, day)
    answer = solution.solve(input, part)

    print(answer)


if __name__ == "__main__":
    main()
