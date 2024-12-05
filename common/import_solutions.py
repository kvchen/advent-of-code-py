import importlib
from pathlib import Path


def import_solutions(base_path: Path) -> None:
    for module_path in base_path.glob("**/day_*.py"):
        importlib.import_module(f"{base_path.name}.{module_path.stem}")
