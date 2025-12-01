"""
Script para corregir metadatos y formato de notebooks
Soluciona:
1. Agrega bloques de metadatos faltantes
2. Corrige tipos de celda incorrectos (code/markdown con language incorrecto)
3. Formatea metadatos para legibilidad
"""
import json
from pathlib import Path
from typing import Dict, List

# Mapeo de notebooks a sus metadatos
NOTEBOOK_METADATA = {
    "DA-01-modelo_dimensional.ipynb": {
        "id": "DA-01",
        "title": "Modelo Dimensional para Supply Chain",
        "specialty": "Data Architecture",
        "process": "Design",
        "level": "Intermediate",
        "tags": ["dimensional", "star-schema", "warehouse", "sql"],
        "estimated_time_min": 60
    },
    "DS-01-eda.ipynb": {
        "id": "DS-01",
        "title": "EDA de órdenes e inventarios",
        "specialty": "Data Science",
        "process": "Discover",
        "level": "Intro",
        "tags": ["eda", "pandas", "plot", "analysis"],
        "estimated_time_min": 30
    },
    "DS-02-estacionalidad.ipynb": {
        "id": "DS-02",
        "title": "Análisis de estacionalidad en demanda",
        "specialty": "Data Science",
        "process": "Discover",
        "level": "Intermediate",
        "tags": ["timeseries", "seasonality", "forecast"],
        "estimated_time_min": 45
    },
    "OR-01-stock_seguridad.ipynb": {
        "id": "OR-01",
        "title": "Cálculo de stock de seguridad",
        "specialty": "Operations Research",
        "process": "Optimize",
        "level": "Intermediate",
        "tags": ["inventory", "safety-stock", "optimization"],
        "estimated_time_min": 45
    },
    "OR-02-vrp_capacidad.ipynb": {
        "id": "OR-02-VRP",
        "title": "Vehicle Routing Problem con capacidad",
        "specialty": "Operations Research",
        "process": "Optimize",
        "level": "Advanced",
        "tags": ["vrp", "routing", "optimization", "pulp"],
        "estimated_time_min": 60
    },
    "RT-01-stream_tracking.ipynb": {
        "id": "RT-01",
        "title": "Streaming de eventos de tracking",
        "specialty": "Real-time IoT",
        "process": "Deliver",
        "level": "Advanced",
        "tags": ["streaming", "iot", "realtime", "kafka"],
        "estimated_time_min": 60
    },
    "GEN-01-rag_kpi.ipynb": {
        "id": "GEN-01",
        "title": "RAG para consultas de KPIs",
        "specialty": "AI & Generative Agents",
        "process": "Innovate",
        "level": "Advanced",
        "tags": ["rag", "llm", "ai", "agents"],
        "estimated_time_min": 60
    }
}

def create_metadata_cell(metadata: Dict) -> Dict:
    """Crea una celda markdown con el bloque de metadatos YAML bien formateado"""
    lines = [
        "---",
        f'id: "{metadata["id"]}"',
        f'title: "{metadata["title"]}"',
        f'specialty: "{metadata["specialty"]}"',
        f'process: "{metadata["process"]}"',
        f'level: "{metadata["level"]}"',
        f'tags: {json.dumps(metadata["tags"])}',
        f'estimated_time_min: {metadata["estimated_time_min"]}',
        "---"
    ]
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["\\n".join(lines) + "\\n"]
    }

def fix_cell_type(cell: Dict) -> Dict:
    """Corrige el tipo de celda basándose en el contenido y metadata"""
    cell_type = cell.get("cell_type", "")
    metadata = cell.get("metadata", {})
    language = metadata.get("language", "")
    
    # Si el tipo y el language no coinciden, corregir
    if cell_type == "code" and language == "markdown":
        cell["cell_type"] = "markdown"
        # Limpiar metadata para markdown
        cell["metadata"] = {}
    elif cell_type == "markdown" and language == "python":
        cell["cell_type"] = "code"
        # Asegurar metadata correcto para code
        cell["metadata"] = {"language": "python"}
    elif cell_type == "markdown" and language == "markdown":
        # Redundante, limpiar
        cell["metadata"] = {}
    
    return cell

def has_metadata_block(notebook: Dict) -> bool:
    """Verifica si el notebook tiene un bloque de metadatos YAML"""
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if source.strip().startswith("---") and 'id: "' in source and 'title: "' in source:
                return True
    return False

def fix_notebook(notebook_path: Path) -> bool:
    """
    Corrige un notebook específico
    Retorna True si se hicieron cambios
    """
    print(f"\n🔍 Procesando: {notebook_path.name}")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    changed = False
    cells = notebook.get("cells", [])
    
    # 1. Corregir tipos de celda incorrectos
    for i, cell in enumerate(cells):
        original_type = cell.get("cell_type")
        original_meta = cell.get("metadata", {}).get("language")
        fixed_cell = fix_cell_type(cell)
        new_type = fixed_cell.get("cell_type")
        new_meta = fixed_cell.get("metadata", {}).get("language")
        
        if new_type != original_type or new_meta != original_meta:
            cells[i] = fixed_cell
            changed = True
            print(f"   ✅ Corregida celda {i+1}: {original_type} ({original_meta}) → {new_type} ({new_meta if new_meta else 'sin language'})")
    
    # 2. Agregar bloque de metadatos si falta
    if notebook_path.name in NOTEBOOK_METADATA and not has_metadata_block(notebook):
        metadata = NOTEBOOK_METADATA[notebook_path.name]
        metadata_cell = create_metadata_cell(metadata)
        
        # Buscar posición ideal (después de setup de entorno y contexto)
        insert_pos = 2 if len(cells) > 2 else 0
        cells.insert(insert_pos, metadata_cell)
        changed = True
        print(f"   ✅ Agregado bloque de metadatos en posición {insert_pos + 1}")
    
    # 3. Guardar cambios si hubo modificaciones
    if changed:
        notebook["cells"] = cells
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"   💾 Guardado: {notebook_path.name}")
        return True
    else:
        print(f"   ⏭️  Sin cambios necesarios")
        return False

def main():
    """Procesa todos los notebooks del proyecto"""
    notebooks_dir = Path(__file__).parent.parent / "notebooks"
    
    print("🚀 Iniciando corrección de notebooks...")
    print(f"📁 Directorio: {notebooks_dir}")
    
    # Buscar todos los notebooks
    notebook_files = list(notebooks_dir.rglob("*.ipynb"))
    print(f"\n📊 Encontrados {len(notebook_files)} notebooks")
    
    # Excluir PLANTILLA y checkpoints
    notebook_files = [
        nb for nb in notebook_files 
        if "PLANTILLA" not in nb.name and ".ipynb_checkpoints" not in str(nb)
    ]
    
    fixed_count = 0
    for nb_path in sorted(notebook_files):
        if fix_notebook(nb_path):
            fixed_count += 1
    
    print(f"\n✅ Proceso completado!")
    print(f"📝 Notebooks corregidos: {fixed_count}/{len(notebook_files)}")

if __name__ == "__main__":
    main()
