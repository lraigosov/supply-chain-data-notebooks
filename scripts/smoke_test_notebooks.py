"""
Lightweight smoke execution of selected notebooks using nbclient.

By default executes a curated subset of notebooks quickly to catch runtime breaks.
Example:
    python scripts/smoke_test_notebooks.py --ids DS-01,BA-01,OR-01
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List, Mapping

import nbformat
import yaml
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "config" / "notebooks_index.yml"

# Default subset covers main domains and runs relatively fast.
DEFAULT_IDS = [
    "DS-01",
    "DS-02",
    "BA-01",
    "OR-01",
    "RT-01",
    "GEN-01",
]


def load_index() -> List[Mapping[str, str]]:
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    notebooks = data.get("notebooks", [])
    if not isinstance(notebooks, list):
        raise ValueError("Expected `notebooks` to be a list in notebooks_index.yml")
    return notebooks


def resolve_paths(index: List[Mapping[str, str]], ids: Iterable[str]) -> List[Path]:
    wanted = set(ids)
    paths: List[Path] = []
    for entry in index:
        nb_id = entry.get("id")
        if nb_id in wanted:
            path = entry.get("path")
            if not path:
                raise ValueError(f"Notebook id {nb_id} missing path")
            paths.append(ROOT / path)
    missing = wanted.difference({entry.get("id") for entry in index})
    if missing:
        raise ValueError(f"Notebook ids not found in index: {', '.join(sorted(missing))}")
    return paths


def execute_notebook(nb_path: Path, timeout: int) -> None:
    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(nb_path.parent)}},
    )
    client.execute()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke test notebooks with nbclient")
    parser.add_argument(
        "--ids",
        type=str,
        default=",".join(DEFAULT_IDS),
        help="Comma-separated notebook IDs to run; defaults to curated subset",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Per-notebook timeout in seconds",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    index = load_index()
    paths = resolve_paths(index, ids)
    failures: List[str] = []
    for nb_path in paths:
        print(f"[SMOKE] Running {nb_path.relative_to(ROOT)} ...")
        try:
            execute_notebook(nb_path, timeout=args.timeout)
        except CellExecutionError as exc:
            failures.append(f"{nb_path.name}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{nb_path.name}: {exc}")
    if failures:
        print("\nFailures detected:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)
    print("\nSmoke tests passed")


if __name__ == "__main__":
    main()
