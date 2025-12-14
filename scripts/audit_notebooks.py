
import json
import re
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(r"f:\GitHub\supply-chain-data-notebooks")
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
REPORT_PATH = BASE_DIR / "reports" / "audit_report.md"

# Patterns to check
CHECKS = {
    "HEADER": r"^# .*$|Title:|id:",  # Title or metadata block
    "OBJECTIVES": r"^## .*Objetivos.*",
    "CONTEXT": r"^## .*Contexto.*|^## .*Qué / Por qué.*",
    "SETUP_IMPORTS": r"import pandas|from src.utils"
}

def analyze_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except:
            return {"ERROR": "JSON Decode Error"}
            
    findings = []
    found_sections = set()
    
    # scan cells
    for cell in nb['cells']:
        source = "".join(cell['source'])
        
        if cell['cell_type'] == 'markdown':
            if re.search(CHECKS["HEADER"], source, re.M): found_sections.add("HEADER")
            if re.search(CHECKS["OBJECTIVES"], source, re.M | re.I): found_sections.add("OBJECTIVES")
            if re.search(CHECKS["CONTEXT"], source, re.M | re.I): found_sections.add("CONTEXT")
        
        if cell['cell_type'] == 'code':
            if re.search(CHECKS["SETUP_IMPORTS"], source): found_sections.add("SETUP_IMPORTS")

    # Determine missing
    missing = []
    for section in ["HEADER", "OBJECTIVES", "CONTEXT", "SETUP_IMPORTS"]:
        if section not in found_sections:
            missing.append(section)
    
    return missing

def main():
    print(f"Auditing notebooks in {NOTEBOOKS_DIR}...")
    
    report = defaultdict(list)
    total = 0
    issues = 0
    
    files = list(NOTEBOOKS_DIR.rglob("*.ipynb"))
    for p in files:
        if ".ipynb_checkpoints" in str(p): continue
        if "PLANTILLA" in p.name or "TEMPLATE" in p.name: continue
        
        total += 1
        missing = analyze_notebook(p)
        if missing:
            issues += 1
            report[p.parent.name].append(f"- [ ] **{p.name}** missing: {', '.join(missing)}")

    # Generate Report
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("# Notebook Formatting Audit Report\n\n")
        f.write(f"**Total Notebooks**: {total}\n")
        f.write(f"**Issues Found**: {issues}\n\n")
        
        for folder, items in sorted(report.items()):
            f.write(f"## {folder}\n")
            for item in sorted(items):
                f.write(f"{item}\n")
            f.write("\n")
            
    print(f"Audit complete. Report saved to {REPORT_PATH}")
    print(f"Found {issues} notebooks with issues.")

if __name__ == "__main__":
    # Ensure report dir exists
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    main()
