"""
Validar que notebooks tengan metadatos mínimos en su primera celda.

Metadatos esperados (YAML en primera celda):
  - title: Título descriptivo
  - objective: Qué se aprende
  - level: Intro, Intermediate, Advanced
  - duration_min: Minutos estimados
  - datasets: Lista de CSVs requeridos
  - tags: Lista de tags
  - author: Quien creó/mantiene

Uso:
  python scripts/validate_notebook_metadata.py
  python scripts/validate_notebook_metadata.py --fix  # Intenta corregir automáticamente
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import nbformat
import yaml

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"

REQUIRED_FIELDS = ["title", "objective", "level", "duration_min", "datasets", "tags"]
OPTIONAL_FIELDS = ["author", "process", "specialty"]


def extract_metadata(nb: nbformat.NotebookNode) -> dict[str, Any]:
    """Extract YAML metadata from first markdown cell."""
    if not nb.cells or nb.cells[0]["cell_type"] != "markdown":
        return {}

    source = "".join(nb.cells[0]["source"])
    
    # Look for YAML block
    if source.startswith("---"):
        lines = source.split("\n")
        end_idx = None
        for i, line in enumerate(lines[1:], 1):
            if line.startswith("---"):
                end_idx = i
                break
        if end_idx:
            yaml_text = "\n".join(lines[1:end_idx])
            try:
                return yaml.safe_load(yaml_text) or {}
            except yaml.YAMLError:
                return {}
    return {}


def validate_notebook(nb_path: Path) -> tuple[bool, list[str]]:
    """Validate a notebook's metadata."""
    try:
        nb = nbformat.read(nb_path, as_version=4)
    except Exception as e:
        return False, [f"Cannot read notebook: {e}"]

    errors = []
    metadata = extract_metadata(nb)

    if not metadata:
        errors.append("No YAML metadata found in first cell")

    for field in REQUIRED_FIELDS:
        if field not in metadata or not metadata[field]:
            errors.append(f"Missing required field: {field}")

    # Validate specific fields
    if "level" in metadata:
        valid_levels = ["Intro", "Intermediate", "Advanced"]
        if metadata["level"] not in valid_levels:
            errors.append(f"Invalid level '{metadata['level']}'. Must be: {', '.join(valid_levels)}")

    if "duration_min" in metadata:
        try:
            int(metadata["duration_min"])
        except (ValueError, TypeError):
            errors.append(f"duration_min must be integer, got: {metadata['duration_min']}")

    if "datasets" in metadata and not isinstance(metadata["datasets"], list):
        errors.append("datasets must be a list")

    if "tags" in metadata and not isinstance(metadata["tags"], list):
        errors.append("tags must be a list")

    return len(errors) == 0, errors


def scan_notebooks() -> dict[Path, tuple[bool, list[str]]]:
    """Scan all notebooks and validate."""
    results = {}
    for nb_path in sorted(NOTEBOOKS_DIR.rglob("*.ipynb")):
        # Skip output notebooks
        if nb_path.name.endswith(".out.ipynb"):
            continue
        # Skip template
        if nb_path.name == "PLANTILLA.ipynb":
            continue
        valid, errors = validate_notebook(nb_path)
        results[nb_path] = (valid, errors)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate notebook metadata")
    parser.add_argument("--fix", action="store_true", help="Attempt automatic fixes (not yet implemented)")
    args = parser.parse_args()

    print("🔍 Validating notebook metadata...\n")

    results = scan_notebooks()
    
    passed = sum(1 for valid, _ in results.values() if valid)
    failed = len(results) - passed

    print(f"Results: {passed} ✓ | {failed} ✗\n")

    has_errors = False
    for nb_path in sorted(results.keys()):
        valid, errors = results[nb_path]
        if not valid:
            has_errors = True
            rel_path = nb_path.relative_to(ROOT)
            print(f"❌ {rel_path}")
            for error in errors:
                print(f"   - {error}")

    if passed == len(results):
        print("✅ All notebooks have valid metadata!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {failed} notebook(s) need attention")
        sys.exit(1)


if __name__ == "__main__":
    main()
