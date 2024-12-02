from pathlib import Path
import click
from common.solution import SolutionBase
from common.import_solutions import import_solutions
from typing import TextIO


@click.command()
@click.option("--year", type=int, default=2024)
@click.option("--day", type=int, required=True)
@click.option("--part", type=click.Choice(list(SolutionBase.Part)), required=True)
@click.option("--input", type=click.File("r"), required=True)
def main(year: int, day: int, part: SolutionBase.Part, input: TextIO):
    base_path = Path(f"solutions_{year}")
    import_solutions(base_path)

    solution = SolutionBase.get_solution(year, day)
    answer = solution.solve(input, part)

    print(answer)


if __name__ == "__main__":
    main()
