
import json
import re
import os
from pathlib import Path

# Paths
BASE_DIR = Path(r"f:\GitHub\supply-chain-data-notebooks")
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# HTML Template - MINIFIED
HTML_TEMPLATE = '<div style="width: 100%; clear: both; margin: 0 0 20px 0; border-top: 1px solid #eaecef; padding-top: 24px;"><div style="display: flex; justify-content: space-between; align-items: center; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif;"><div style="flex: 1; text-align: left;">{prev_content}</div><div style="flex: 1; text-align: center; font-size: 14px;"><a href="../../README.md" style="color: #0366d6; text-decoration: none; font-weight: 600; margin: 0 10px;">📑 Índice</a><span style="color: #6a737d;">|</span><a href="../../config/notebooks_index.yml" style="color: #0366d6; text-decoration: none; font-weight: 600; margin: 0 10px;">📋 Catálogo</a></div><div style="flex: 1; text-align: right;">{next_content}</div></div></div>'
BUTTON_TEMPLATE = '<a href="{url}" style="text-decoration: none; color: #0366d6; font-size: 14px; font-weight: 600; transition: color 0.2s;">{inner_html}</a>'
DISABLED_TEMPLATE = '<span style="color: #6a737d; font-size: 14px; cursor: default;">{text}</span>'

def normalize_text(text):
    return " ".join(text.split())

def generate_button(link_data, direction="prev"):
    if not link_data["active"] or not link_data["url"]:
        if direction == "prev": return DISABLED_TEMPLATE.format(text="← Anterior")
        else: return DISABLED_TEMPLATE.format(text="Siguiente →")
    
    label = link_data['label']
    url = link_data['url']
    if direction == "prev": inner = f'← Anterior: {label}'
    else: inner = f'Siguiente: {label} →'
    return BUTTON_TEMPLATE.format(url=url, inner_html=inner)

def build_notebook_map():
    mapping = {}
    print("Building notebook map...")
    for p in NOTEBOOKS_DIR.rglob("*.ipynb"):
        if ".ipynb_checkpoints" in str(p): continue
        m = re.match(r"^([A-Z]{2,4}-\d{2})", p.name)
        key = m.group(1) if m else p.stem.upper()
        mapping[key] = p
    print(f"Mapped {len(mapping)} notebooks.")
    return mapping

def resolve_url(label, current_file_path, nb_map):
    if not label: return None
    clean_label = label.strip()
    target_path = nb_map.get(clean_label)
    
    # Fuzzy match logic
    if not target_path:
        # If label contains ID e.g. "Ingesta (DE-01)"
        m = re.search(r"([A-Z]{2,4}-\d{2})", clean_label)
        if m: target_path = nb_map.get(m.group(1))

    if not target_path: return None
    
    try:
        rel_path = os.path.relpath(target_path, current_file_path.parent)
        return rel_path.replace("\\", "/")
    except ValueError: return None

NOTEBOOK_MAP = build_notebook_map()

def process_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError: return

    changed = False
    
    for cell in reversed(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source_raw = "".join(cell['source'])
            
            # Detect Navigation Block OR Resources List (Fallback)
            is_nav_block = "📚 Navegación" in source_raw
            is_resource_list = "📋 Recursos" in source_raw and "Índice del proyecto" in source_raw
            
            if is_nav_block or is_resource_list:
                
                # --- EXTRACTION ---
                text_only = re.sub(r'<[^>]+>', ' ', source_raw)
                text_only = normalize_text(text_only)
                
                prev_label = None
                next_label = None

                m_prev = re.search(r"Anterior:?\s*(.*?)($|\s*\||\s*Siguiente)", text_only)
                if m_prev:
                    lbl = m_prev.group(1).replace("←", "").replace("|", "").strip()
                    if "Índice" in lbl: lbl = lbl.split("Índice")[0].strip()
                    if "https" in lbl: lbl = ""
                    if lbl and lbl != "—": prev_label = lbl

                m_next = re.search(r"Siguiente:?\s*(.*?)($|\s*→)", text_only)
                if m_next:
                    lbl = m_next.group(1).replace("→", "").strip()
                    if "https" in lbl: lbl = ""
                    if lbl and lbl != "—": next_label = lbl

                # Fallback: if Resources list, we assume we lost the labels or they weren't there.
                # But we can try to guess from file name? E.g. DE-01 -> Prev=False, Next=DE-02
                # For now let's just make it empty if we can't find them, but formatted correctly.
                
                # --- AUTO-LINKING BASED ON ID SEQUENCE ---
                # If we have an ID like DE-01, we can try to find DE-00 or DE-02
                current_id = None
                m_curr = re.match(r"^([A-Z]{2,4}-\d{2})", filepath.name)
                if m_curr:
                    current_id = m_curr.group(1)
                    prefix = current_id.split("-")[0]
                    num = int(current_id.split("-")[1])
                    
                    if not prev_label:
                        prev_candidate = f"{prefix}-{num-1:02d}"
                        if prev_candidate in NOTEBOOK_MAP: prev_label = prev_candidate
                    
                    if not next_label:
                        next_candidate = f"{prefix}-{num+1:02d}"
                        if next_candidate in NOTEBOOK_MAP: next_label = next_candidate
                
                # --- SPECIAL CASE: PLANTILLA/TEMPLATE ---
                if "PLANTILLA" in filepath.name or "TEMPLATE" in filepath.name:
                    prev_label = None
                    next_label = None

                # --- RESOLUTION ---
                prev_url = resolve_url(prev_label, filepath, NOTEBOOK_MAP)
                next_url = resolve_url(next_label, filepath, NOTEBOOK_MAP)
                
                prev_data = {"active": bool(prev_url), "url": prev_url, "label": prev_label or ""}
                next_data = {"active": bool(next_url), "url": next_url, "label": next_label or ""}
                
                # --- GENERATION ---
                prev_btn = generate_button(prev_data, "prev")
                next_btn = generate_button(next_data, "next")
                new_html = HTML_TEMPLATE.format(prev_content=prev_btn, next_content=next_btn)
                
                # Check for change
                old_clean = "".join(source_raw.split())
                new_clean = "".join(new_html.split())
                has_indentation = any(line.startswith(' ') for line in cell['source'])
                
                if old_clean != new_clean or has_indentation:
                    cell['source'] = [new_html]
                    changed = True
                    print(f"Updated {filepath.name}: P='{prev_label}' N='{next_label}'")
                
                break

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')

def main():
    print(f"Scanning {NOTEBOOKS_DIR}...")
    files = list(NOTEBOOKS_DIR.rglob("*.ipynb"))
    for p in files:
        if ".ipynb_checkpoints" in str(p): continue
        process_notebook(p)

if __name__ == "__main__":
    main()
