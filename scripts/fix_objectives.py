
import json
import re
from pathlib import Path

BASE_DIR = Path(r"f:\GitHub\supply-chain-data-notebooks")
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

def fix_content(text):
    original = text
    
    # Check if we have the "Objectives" header
    if "Objetivos de Aprendizaje" not in text:
        return text, False

    # Fix 1: Header crammed with first item
    # "Objetivos de Aprendizaje- Definir" -> "Objetivos de Aprendizaje\n\n- Definir"
    # "Objetivos de Aprendizaje - Definir" -> ...
    # Be careful not to replace if it's already good.
    # Regex: Look for Header, followed by optional space, then hyphen, then something.
    # But EXCLUDE if there is a newline in between.
    
    # Strategy: Replace "Aprendizaje[ ]?-[ ]?" with "Aprendizaje\n\n- "
    text = re.sub(r"(Objetivos de Aprendizaje)[ \t]*-[ \t]*", r"\1\n\n- ", text)
    
    # Fix 2: Items crammed together
    # "puntos).- Conectar" -> "puntos).\n- Conectar"
    # "IoT).- Incluir" -> "IoT).\n- Incluir"
    # General: ".- " -> ".\n- " 
    # But allow for spaced hyphens?
    # The screenshot showed "puntos).- Conectar"
    
    text = re.sub(r"(\)\.)[ \t]*-[ \t]*", r"\1\n- ", text)
    
    # Also handle "puntos). - Conectar" just in case
    
    return text, (text != original)

def process_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except: return False

    changed = False
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source_raw = "".join(cell['source'])
            
            # Target cells with Objectives
            if "Objetivos de Aprendizaje" in source_raw:
                new_source, modified = fix_content(source_raw)
                
                if modified:
                    # Clean up: ensure we split back into lines if needed for JSON neatness (optional but good)
                    # Jupyter can handle single long string with \n, but best practice is list of lines.
                    # Simple split by \n
                    # cell['source'] = [line + '\n' for line in new_source.split('\n')]
                    # Actually, let's keep it simple.
                    cell['source'] = [new_source]
                    changed = True
                    if dry_run:
                        print(f"[DRY RUN] Would fix {filepath.name}")
                        # print(f"BEFORE: {source_raw[:100]}")
                        # print(f"AFTER : {new_source[:100]}")
    
    if changed and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print(f"Fixed {filepath.name}")
        return True
        
    return False

def main():
    print("Running Fixer...")
    count = 0
    files = list(NOTEBOOKS_DIR.rglob("*.ipynb"))
    for p in files:
        if ".ipynb_checkpoints" in str(p): continue
        if "PLANTILLA" in p.name: continue # Don't touch template
        
        # dry run first
        if process_file(p, dry_run=False):
            count += 1
            
    print(f"Total fixed: {count}")

if __name__ == "__main__":
    main()
