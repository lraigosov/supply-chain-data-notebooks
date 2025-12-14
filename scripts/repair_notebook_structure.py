
import json
import re
from pathlib import Path

# Paths
BASE_DIR = Path(r"f:\GitHub\supply-chain-data-notebooks")
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
REPORT_PATH = BASE_DIR / "reports" / "audit_report.md"

# Placeholders
CONTEXT_PLACEHOLDER = """## Contexto de Negocio
> **TODO**: Describir brevemente el contexto, el problema a resolver y el valor para el negocio (Qué, Por qué, Para qué).
"""

OBJECTIVES_PLACEHOLDER = """## 🎯 Objetivos de Aprendizaje
- [ ] Objetivo 1
- [ ] Objetivo 2
"""

# Regex
HEADER_REGEX = r"^# .*$|Title:|id:"

def repair_notebook(filepath, missing_sections):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    cells = nb['cells']
    new_cells = []
    
    # Logic:
    # 1. Find Header cell (usually first or second)
    # 2. Insert Objectives after Header if missing
    # 3. Insert Context after Objectives (or Header) if missing
    # 4. Filter original cells to avoid duplication if I used fuzzy matches before? 
    #    (Audit used Check presence, so if missing, it's safe to add)
    
    # Let's rebuild the list carefully.
    
    # Find insertion point index
    insert_idx = 0
    for i, cell in enumerate(cells):
        src = "".join(cell['source'])
        if re.search(HEADER_REGEX, src, re.M):
            insert_idx = i + 1
            break
            
    # Copy up to insertion point
    new_cells.extend(cells[:insert_idx])
    
    # Insert missing sections
    if "OBJECTIVES" in missing_sections:
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [OBJECTIVES_PLACEHOLDER]
        })
        print(f"Added OBJECTIVES to {filepath.name}")

    if "CONTEXT" in missing_sections:
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [CONTEXT_PLACEHOLDER]
        })
        print(f"Added CONTEXT to {filepath.name}")
        
    # Copy remaining
    new_cells.extend(cells[insert_idx:])
    
    nb['cells'] = new_cells
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')

def main():
    # Read Report to know what to fix? 
    # Or just re-scan with the same logic? Re-scanning is safer.
    from audit_notebooks import analyze_notebook
    
    print(" repairing...")
    count = 0
    files = list(NOTEBOOKS_DIR.rglob("*.ipynb"))
    for p in files:
        if ".ipynb_checkpoints" in str(p): continue
        if "PLANTILLA" in p.name or "TEMPLATE" in p.name: continue
        
        missing = analyze_notebook(p)
        if missing:
            repair_notebook(p, missing)
            count += 1
            
    print(f"Repaired {count} notebooks.")

if __name__ == "__main__":
    main()
