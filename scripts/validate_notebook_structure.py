import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

REPO_ROOT = Path(__file__).resolve().parents[1]
NB_ROOT = REPO_ROOT / "notebooks"
OUTPUT_CSV = REPO_ROOT / "docs" / "notebook_structure_audit.csv"

REQUIRED_SECTIONS = {
    "objetivos": ["objetivos de aprendizaje", "objetivos"],
    "conclusiones": ["conclusiones"],
    "operacion": ["notas de operación", "notas de operacion", "operación", "operacion"]
}

PLACEHOLDER_TITLE = [
    "# <ID> · <Título del Notebook>",
    "",
    "Reemplaza `<ID>` por el código (p. ej., DS-06) y `<Título del Notebook>` por un nombre claro.",
]

PLACEHOLDER_OBJECTIVES = [
    "## 🎯 Objetivos de Aprendizaje",
    "",
    "- Definir qué aprenderá el lector (máx. 5–7 puntos).",
    "- Conectar con el caso de uso del dominio (demanda, logística, IoT).",
    "- Incluir resultados verificables (métricas, validaciones, artefactos generados).",
]

PLACEHOLDER_NOTES = [
    "## 📝 Notas de Operación (Costes, Retención, Gobernanza)",
    "",
    "**Costes**",
    "- Consideraciones de almacenamiento/cómputo/visualización.",
    "",
    "**Retención**",
    "- Política por zonas (raw/curated/analytics) y ventanas temporales.",
    "",
    "**Gobernanza**",
    "- Calidad de datos, seguridad/PII, linaje, versionado de modelos/artefactos.",
]

PLACEHOLDER_CONCLUSIONS = [
    "## 🎓 Conclusiones",
    "",
    "- Resumen de hallazgos y métricas clave.",
    "- Buenas prácticas y siguientes pasos.",
]

def normalize_text(s: str) -> str:
    s = s.lower()
    # naive accent handling
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")]:
        s = s.replace(a, b)
    return s

def derive_id_and_title(path: Path) -> (str, str):
    """Deriva ID (prefijo) y título legible desde el nombre del archivo."""
    base = path.stem  # e.g., DS-06-forecast_arima
    parts = base.split("-")
    if len(parts) >= 2:
        nb_id = parts[0]
        title_tokens = parts[1:]
    else:
        nb_id = parts[0]
        title_tokens = []

    title_raw = " ".join(title_tokens).replace("_", " ").strip()
    if not title_raw:
        title_raw = "Notebook"

    # Capitalizar palabras y preservar acrónimos comunes
    words = title_raw.split()
    acronyms = {
        "arima": "ARIMA",
        "sarima": "SARIMA",
        "iot": "IoT",
        "kpi": "KPI",
        "or": "OR",
        "ai": "AI",
        "bi": "BI",
        "rag": "RAG",
        "vrp": "VRP",
    }
    styled = []
    for w in words:
        lw = w.lower()
        if lw in acronyms:
            styled.append(acronyms[lw])
        else:
            styled.append(w.capitalize())
    title = " ".join(styled)
    return nb_id, title

def cell_contains(cell: Dict, needles: List[str]) -> bool:
    if not isinstance(cell, dict):
        return False
    if cell.get("cell_type") != "markdown":
        return False
    lines = cell.get("source", [])
    text = "\n".join([str(x) for x in lines])
    norm = normalize_text(text)
    return any(n in norm for n in needles)

def first_heading(cell: Dict) -> str:
    if cell.get("cell_type") != "markdown":
        return ""
    for line in cell.get("source", []):
        s = str(line).strip()
        if s.startswith("# "):
            return s
    return ""

def has_title_first_cell(cells: List[Dict]) -> bool:
    if not cells:
        return False
    first = cells[0]
    if first.get("cell_type") != "markdown":
        return False
    src = first.get("source", [])
    return any(str(line).strip().startswith("# ") or str(line).strip().startswith("#\t") for line in src)

def audit_notebook(path: Path) -> Dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        # some ipynb may have standard fields; fallback to json.load
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    cells = data.get("cells", [])
    # counts and simple signals
    code_cells = sum(1 for c in cells if c.get("cell_type") == "code")
    md_cells = sum(1 for c in cells if c.get("cell_type") == "markdown")
    executed = sum(1 for c in cells if c.get("cell_type") == "code" and c.get("execution_count"))

    result = {
        "path": str(path.relative_to(REPO_ROOT)),
        "has_title": has_title_first_cell(cells),
        "has_obj": any(cell_contains(c, REQUIRED_SECTIONS["objetivos"]) for c in cells),
        "has_conc": any(cell_contains(c, REQUIRED_SECTIONS["conclusiones"]) for c in cells),
        "has_ops": any(cell_contains(c, REQUIRED_SECTIONS["operacion"]) for c in cells),
        "heading": first_heading(cells[0]) if cells else "",
        "code_cells": code_cells,
        "md_cells": md_cells,
        "executed_code_cells": executed,
        "uses_data_raw": any("data/raw" in "\n".join(map(str, c.get("source", []))) for c in cells),
        "imports_plotly": any("plotly" in "\n".join(map(str, c.get("source", []))) for c in cells),
        "fixes": 0,
    }
    return result

def apply_fixes(path: Path) -> int:
    # returns number of fixes applied
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    cells = data.get("cells", [])

    has_title = has_title_first_cell(cells)
    nb_id, nb_title = derive_id_and_title(path)
    title_line = f"# {nb_id} · {nb_title}"
    has_obj = any(cell_contains(c, REQUIRED_SECTIONS["objetivos"]) for c in cells)
    has_conc = any(cell_contains(c, REQUIRED_SECTIONS["conclusiones"]) for c in cells)
    has_ops = any(cell_contains(c, REQUIRED_SECTIONS["operacion"]) for c in cells)

    fixes = 0

    def new_md_cell(lines: List[str]) -> Dict:
        return {
            "cell_type": "markdown",
            "metadata": {"language": "markdown"},
            "source": lines,
        }

    # Insertar título como primera celda si falta
    if not has_title:
        cells.insert(0, new_md_cell([title_line, ""]))
        fixes += 1
    else:
        # Reemplazar placeholder si existe en la primera celda
        first = cells[0]
        if first.get("cell_type") == "markdown":
            src = list(first.get("source", []))
            norm_first = "\n".join(src)
            if "<ID>" in norm_first or "<Título" in norm_first or "<Titulo" in norm_first:
                # Sustituir encabezado y remover línea de instrucción
                if src:
                    src[0] = title_line
                else:
                    src = [title_line, ""]
                src = [line for line in src if "Reemplaza" not in str(line)]
                first["source"] = src
                fixes += 1

    if not has_obj:
        # insert after first cell if exists, else at top
        idx = 1 if cells else 0
        cells.insert(idx, new_md_cell(PLACEHOLDER_OBJECTIVES))
        fixes += 1
    if not has_ops:
        cells.append(new_md_cell(PLACEHOLDER_NOTES))
        fixes += 1
    if not has_conc:
        cells.append(new_md_cell(PLACEHOLDER_CONCLUSIONS))
        fixes += 1

    if fixes:
        data["cells"] = cells
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return fixes

def write_csv(rows: List[Dict], csv_path: Path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "path", "has_title", "heading", "has_obj", "has_conc", "has_ops",
        "code_cells", "md_cells", "executed_code_cells", "uses_data_raw", "imports_plotly", "fixes"
    ]
    with csv_path.open("w", encoding="utf-8") as f:
        f.write(",".join(headers) + "\n")
        for r in rows:
            f.write(",".join(str(r[h]) for h in headers) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Validate notebook structure vs template")
    parser.add_argument("--fix", action="store_true", help="Apply missing sections placeholders")
    parser.add_argument("--include", nargs="*", default=None, help="Glob patterns to include (default: notebooks/**/.ipynb)")
    args = parser.parse_args()

    patterns = args.include or ["**/*.ipynb"]
    rows = []

    for pat in patterns:
        for nb in NB_ROOT.glob(pat):
            # skip the template itself? We'll include it in report
            try:
                res = audit_notebook(nb)
                if args.fix:
                    res["fixes"] = apply_fixes(nb)
                rows.append(res)
            except Exception as e:
                rows.append({
                    "path": str(nb.relative_to(REPO_ROOT)),
                    "has_title": False,
                    "has_obj": False,
                    "has_conc": False,
                    "has_ops": False,
                    "fixes": f"error:{e}",
                })

    write_csv(rows, OUTPUT_CSV)
    print(f"Audit written: {OUTPUT_CSV}")
    missing = [r for r in rows if not (r["has_title"] and r["has_obj"] and r["has_conc"] and r["has_ops"]) ]
    print(f"Total notebooks: {len(rows)} | Missing structure: {len(missing)}")
    if args.fix:
        total_fixes = sum(int(r["fixes"]) if str(r["fixes"]).isdigit() else 0 for r in rows)
        print(f"Fixes applied: {total_fixes}")

if __name__ == "__main__":
    sys.exit(main())
