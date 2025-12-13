"""
CLI para navegar y ejecutar notebooks del catálogo.

Utilidades:
  - Listar notebooks por especialidad, nivel, tags, o búsqueda libre
  - Ejecutar un notebook individual o lote con papermill
  - Ver metadatos (datasets requeridos, tiempo estimado, etc.)

Ejemplos:
  python -m scripts.catalog list                          # Lista todos
  python -m scripts.catalog list --specialty "Data Science"
  python -m scripts.catalog list --level Intro
  python -m scripts.catalog list --tags eda,pandas
  python -m scripts.catalog search "inventory"
  python -m scripts.catalog show DS-01
  python -m scripts.catalog run DS-01
  python -m scripts.catalog run DS-01,DS-02 --timeout 600
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List, Mapping

import yaml

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "config" / "notebooks_index.yml"


def load_index() -> List[Mapping]:
    """Load notebooks from index YAML."""
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    notebooks = data.get("notebooks", [])
    if not isinstance(notebooks, list):
        raise ValueError("Expected `notebooks` to be a list in notebooks_index.yml")
    return notebooks


def filter_notebooks(
    index: List[Mapping],
    specialty: str | None = None,
    level: str | None = None,
    tags: list[str] | None = None,
    search: str | None = None,
) -> List[Mapping]:
    """Filter notebooks by criteria."""
    result = index
    if specialty:
        result = [nb for nb in result if nb.get("specialty", "").lower() == specialty.lower()]
    if level:
        result = [nb for nb in result if nb.get("level", "").lower() == level.lower()]
    if tags:
        tag_set = set(t.lower() for t in tags)
        result = [
            nb
            for nb in result
            if tag_set.intersection(set(t.lower() for t in nb.get("tags", [])))
        ]
    if search:
        search_lower = search.lower()
        result = [
            nb
            for nb in result
            if search_lower in nb.get("title", "").lower()
            or search_lower in nb.get("id", "").lower()
            or search_lower in " ".join(nb.get("tags", [])).lower()
        ]
    return result


def display_notebook(nb: Mapping, full: bool = False) -> None:
    """Pretty-print a notebook entry."""
    nb_id = nb.get("id", "")
    title = nb.get("title", "")
    specialty = nb.get("specialty", "")
    level = nb.get("level", "")
    path = nb.get("path", "")
    tags = nb.get("tags", [])
    datasets = nb.get("dataset_deps", [])
    time_min = nb.get("estimated_time_min", "")
    process = nb.get("process", "")

    print(f"[{nb_id}] {title}")
    print(f"    Especialidad: {specialty} | Nivel: {level}")
    if process:
        print(f"    Proceso: {process}")
    if tags:
        print(f"    Tags: {', '.join(tags)}")
    if time_min:
        print(f"    Duración estimada: ~{time_min} min")
    if datasets:
        print(f"    Datasets: {', '.join(datasets)}")
    if full and path:
        print(f"    Ruta: {path}")


def cmd_list(args: argparse.Namespace) -> None:
    """List notebooks matching filters."""
    index = load_index()
    filtered = filter_notebooks(
        index,
        specialty=args.specialty,
        level=args.level,
        tags=args.tags,
    )
    if not filtered:
        print("No notebooks matched the filters.")
        return
    print(f"\nEncontrados {len(filtered)} notebooks:\n")
    for nb in filtered:
        display_notebook(nb)
        print()


def cmd_search(args: argparse.Namespace) -> None:
    """Search notebooks by text query."""
    index = load_index()
    filtered = filter_notebooks(index, search=args.query)
    if not filtered:
        print(f"No notebooks matched '{args.query}'.")
        return
    print(f"\nEncontrados {len(filtered)} notebooks:\n")
    for nb in filtered:
        display_notebook(nb)
        print()


def cmd_show(args: argparse.Namespace) -> None:
    """Show details of a specific notebook."""
    index = load_index()
    target = next((nb for nb in index if nb.get("id") == args.id), None)
    if not target:
        print(f"Notebook {args.id} not found.")
        sys.exit(1)
    display_notebook(target, full=True)


def cmd_run(args: argparse.Namespace) -> None:
    """Run one or more notebooks with papermill."""
    import subprocess

    index = load_index()
    ids = [part.strip() for part in args.ids.split(",") if part.strip()]
    notebooks = [next((nb for nb in index if nb.get("id") == nb_id), None) for nb_id in ids]
    missing = [nb_id for nb_id, nb in zip(ids, notebooks) if nb is None]
    if missing:
        print(f"Notebooks not found: {', '.join(missing)}")
        sys.exit(1)

    for nb in notebooks:
        nb_path = ROOT / nb.get("path")
        output_path = nb_path.parent / f"{nb_path.stem}.out.ipynb"
        print(f"\n[RUN] Executing {nb.get('id')}: {nb_path}")
        try:
            result = subprocess.run(
                [
                    "papermill",
                    str(nb_path),
                    str(output_path),
                    "--timeout",
                    str(args.timeout),
                    "--kernel",
                    "python3",
                ],
                check=True,
            )
            print(f"✓ Output saved to {output_path}")
        except subprocess.CalledProcessError as exc:
            print(f"✗ Failed with exit code {exc.returncode}")
            if not args.continue_on_error:
                sys.exit(1)


def main() -> None:
    """Parse arguments and dispatch to subcommand."""
    parser = argparse.ArgumentParser(
        description="Manage and run notebooks from the supply chain catalog",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python -m scripts.catalog list --specialty 'Data Science'\n"
        "  python -m scripts.catalog search inventory\n"
        "  python -m scripts.catalog run DS-01,DS-02\n",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    list_parser = subparsers.add_parser("list", help="List notebooks with optional filters")
    list_parser.add_argument(
        "--specialty",
        type=str,
        help="Filter by specialty (e.g., 'Data Science', 'Optimization & OR')",
    )
    list_parser.add_argument(
        "--level",
        type=str,
        help="Filter by level (Intro, Intermediate, Advanced)",
    )
    list_parser.add_argument(
        "--tags",
        type=str,
        help="Comma-separated tags to match any",
    )
    list_parser.set_defaults(func=cmd_list)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search notebooks by text")
    search_parser.add_argument("query", help="Search query (title, ID, or tags)")
    search_parser.set_defaults(func=cmd_search)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show details of a notebook")
    show_parser.add_argument("id", help="Notebook ID")
    show_parser.set_defaults(func=cmd_show)

    # Run command
    run_parser = subparsers.add_parser("run", help="Execute one or more notebooks")
    run_parser.add_argument("ids", help="Comma-separated notebook IDs")
    run_parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout per notebook in seconds (default: 600)",
    )
    run_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running remaining notebooks if one fails",
    )
    run_parser.set_defaults(func=cmd_run)

    args = parser.parse_args()
    if hasattr(args, "tags") and args.tags:
        args.tags = [t.strip() for t in args.tags.split(",")]
    args.func(args)


if __name__ == "__main__":
    main()
