"""
Script para añadir sección de navegación al final de todos los notebooks.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# Rutas base
ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"
CONFIG_FILE = ROOT / "config" / "notebooks_index.yml"

def load_notebook_index() -> List[Dict]:
    """Carga el índice de notebooks desde el archivo YAML."""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['notebooks']

def get_navigation_links(notebook_id: str, notebook_index: List[Dict]) -> tuple:
    """
    Determina los enlaces de navegación para un notebook dado.
    Retorna (id_anterior, id_siguiente, path_anterior, path_siguiente).
    """
    # Encontrar el índice actual
    current_idx = None
    for idx, nb in enumerate(notebook_index):
        if nb['id'] == notebook_id:
            current_idx = idx
            break
    
    if current_idx is None:
        return None, None, None, None
    
    # Anterior y siguiente
    prev_nb = notebook_index[current_idx - 1] if current_idx > 0 else None
    next_nb = notebook_index[current_idx + 1] if current_idx < len(notebook_index) - 1 else None
    
    prev_id = prev_nb['id'] if prev_nb else None
    next_id = next_nb['id'] if next_nb else None
    prev_path = prev_nb['path'] if prev_nb else None
    next_path = next_nb['path'] if next_nb else None
    
    return prev_id, next_id, prev_path, next_path

def create_navigation_cell(notebook_id: str, notebook_path: str, notebook_index: List[Dict]) -> str:
    """Crea el contenido markdown de la celda de navegación."""
    prev_id, next_id, prev_path, next_path = get_navigation_links(notebook_id, notebook_index)
    
    # Calcular rutas relativas desde el notebook actual
    current_path = Path(notebook_path)
    readme_rel = Path("..") / ".." / "README.md"
    catalog_rel = Path("..") / ".." / "config" / "notebooks_index.yml"
    
    # Construir enlaces de navegación
    nav_parts = []
    
    if prev_id and prev_path:
        # Calcular ruta relativa al notebook anterior
        prev_abs = ROOT / prev_path
        current_abs = ROOT / notebook_path
        try:
            prev_rel = Path("..") / prev_abs.parent.name / prev_abs.name
        except:
            prev_rel = prev_path
        nav_parts.append(f"← Anterior: [{prev_id}]({prev_rel})")
    else:
        nav_parts.append("← Anterior: `—`")
    
    if next_id and next_path:
        # Calcular ruta relativa al notebook siguiente
        next_abs = ROOT / next_path
        current_abs = ROOT / notebook_path
        try:
            next_rel = Path("..") / next_abs.parent.name / next_abs.name
        except:
            next_rel = next_path
        nav_parts.append(f"Siguiente: [{next_id}]({next_rel}) →")
    else:
        nav_parts.append("Siguiente: `—` →")
    
    navigation_md = f"""---

## 📚 Navegación

**[📑 Índice del Proyecto]({readme_rel})** | **[📋 Catálogo de Notebooks]({catalog_rel})**

{" | ".join(nav_parts)}"""
    
    return navigation_md

def has_navigation_section(notebook_path: Path) -> bool:
    """Verifica si el notebook ya tiene una sección de navegación."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        for cell in content.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '## 📚 Navegación' in source or '## Navegación' in source:
                    return True
        return False
    except Exception as e:
        print(f"Error verificando {notebook_path}: {e}")
        return False

def add_navigation_to_notebook(notebook_path: Path, navigation_md: str) -> bool:
    """Añade la celda de navegación al final del notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Verificar si ya existe navegación
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '## 📚 Navegación' in source:
                    print(f"  ⏭️  Ya tiene navegación, omitiendo...")
                    return False
        
        # Crear nueva celda de navegación
        nav_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": navigation_md.split('\n')
        }
        
        # Añadir al final
        notebook['cells'].append(nav_cell)
        
        # Guardar
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, ensure_ascii=False, indent=1)
        
        return True
    except Exception as e:
        print(f"  ❌ Error procesando {notebook_path}: {e}")
        return False

def main():
    """Procesa todos los notebooks añadiendo navegación."""
    print("🚀 Añadiendo navegación a notebooks...\n")
    
    # Cargar índice
    notebook_index = load_notebook_index()
    print(f"📋 Cargados {len(notebook_index)} notebooks del índice\n")
    
    # Crear un mapa de path -> id
    path_to_id = {nb['path']: nb['id'] for nb in notebook_index}
    
    # Contadores
    processed = 0
    skipped = 0
    errors = 0
    
    # Procesar cada notebook del índice
    for nb in notebook_index:
        notebook_id = nb['id']
        notebook_path = ROOT / nb['path']
        
        if not notebook_path.exists():
            print(f"⚠️  {notebook_id}: Archivo no encontrado - {notebook_path}")
            errors += 1
            continue
        
        print(f"📓 {notebook_id}: {nb['title']}")
        
        # Crear contenido de navegación
        navigation_md = create_navigation_cell(notebook_id, nb['path'], notebook_index)
        
        # Añadir al notebook
        if add_navigation_to_notebook(notebook_path, navigation_md):
            print(f"  ✅ Navegación añadida\n")
            processed += 1
        else:
            skipped += 1
            print()
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"✅ Procesados: {processed}")
    print(f"⏭️  Omitidos: {skipped}")
    print(f"❌ Errores: {errors}")
    print(f"📊 Total: {len(notebook_index)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
