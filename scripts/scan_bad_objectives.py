
import json
import re
from pathlib import Path

BASE_DIR = Path(r"f:\GitHub\supply-chain-data-notebooks")
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

def main():
    print("Scanning for malformed Objectives headers...")
    
    bad_files = []
    
    for p in NOTEBOOKS_DIR.rglob("*.ipynb"):
        if ".ipynb_checkpoints" in str(p): continue
        if "PLANTILLA" in p.name: continue
        
        with open(p, 'r', encoding='utf-8') as f:
            try:
                nb = json.load(f)
            except: continue
            
        for cell in nb['cells']:
            if cell['cell_type'] == 'markdown':
                src = "".join(cell['source'])
                
                # Check for "Objetivos" followed immediately by content on the same line or concatenated
                # Pattern from screenshot: "Objetivos de Aprendizaje- Definir"
                
                if "Objetivos de Aprendizaje" in src:
                    # Check if it has the specific cramped pattern
                    # "Aprendizaje- " or "Aprendizaje -"
                    if re.search(r"Objetivos de Aprendizaje\s*-\s*Definir", src):
                         print(f"FOUND MATCH in {p.name}")
                         print(f"  Snippet: {src[:100]}...")
                         bad_files.append(p)
                    # Check for "Header - Item" generally
                    elif re.search(r"^#+.*Objetivos.*?- ", src, re.M):
                         print(f"FOUND GENERIC MATCH in {p.name}")
                         bad_files.append(p)
                    
    print(f"Found {len(bad_files)} potentially bad files.")

if __name__ == "__main__":
    main()
