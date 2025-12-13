"""
Generate the notebooks catalog table for README from config/notebooks_index.yml.
Usage:
    python scripts/generate_notebook_catalog.py
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Mapping

import yaml

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "config" / "notebooks_index.yml"
README_PATH = ROOT / "README.md"

START_MARKER = "<!-- NOTEBOOKS-TABLE:START -->"
END_MARKER = "<!-- NOTEBOOKS-TABLE:END -->"


def load_notebooks() -> List[Mapping[str, str]]:
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    notebooks = data.get("notebooks", [])
    if not isinstance(notebooks, list):
        raise ValueError("Expected `notebooks` to be a list in notebooks_index.yml")
    return notebooks


def render_table_rows(notebooks: Iterable[Mapping[str, str]]) -> str:
    header = "| ID | Título | Especialidad | Nivel | Notebook |"
    separator = "| --- | --- | --- | --- | --- |"
    lines = [header, separator]
    for nb in notebooks:
        nb_id = nb.get("id", "")
        title = nb.get("title", "")
        specialty = nb.get("specialty", "")
        level = nb.get("level", "")
        path = nb.get("path", "")
        link = f"[{Path(path).name}]({path})" if path else ""
        lines.append(f"| {nb_id} | {title} | {specialty} | {level} | {link} |")
    return "\n".join(lines)


def replace_block(readme_text: str, block: str) -> str:
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        raise ValueError("Markers not found in README. Add START and END markers before running.")
    pre, _, rest = readme_text.partition(START_MARKER)
    _, _, post = rest.partition(END_MARKER)
    return f"{pre}{START_MARKER}\n{block}\n{END_MARKER}{post}"


def main() -> None:
    notebooks = load_notebooks()
    table = render_table_rows(notebooks)
    readme_text = README_PATH.read_text(encoding="utf-8")
    updated = replace_block(readme_text, table)
    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
