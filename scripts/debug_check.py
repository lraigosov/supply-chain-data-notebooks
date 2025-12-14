
import json
import re
from pathlib import Path

FILE = Path(r"f:\GitHub\supply-chain-data-notebooks\notebooks\10_data_engineering\DE-01-ingesta.ipynb")

def debug():
    with open(FILE, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Check last few cells
    for i, cell in enumerate(nb['cells'][-3:]):
        print(f"--- CELL -{3-i} ---")
        src = "".join(cell['source'])
        print(src)
        print("HAS NAV?", "📚 Navegación" in src)
        
        text_only = re.sub(r'<[^>]+>', ' ', src)
        print("TEXT ONLY:", text_only.strip())
        
if __name__ == "__main__":
    debug()
