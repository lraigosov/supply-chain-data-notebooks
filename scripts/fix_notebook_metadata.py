"""
Script MEJORADO para corregir metadatos y formato de notebooks
Soluciona:
1. Agrega bloques de metadatos faltantes
2. Corrige tipos de celda basándose en el CONTENIDO real
3. Formatea metadatos para legibilidad
"""
import json
import re
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
        "---\\n",
        f'id: "{metadata["id"]}"\\n',
        f'title: "{metadata["title"]}"\\n',
        f'specialty: "{metadata["specialty"]}"\\n',
        f'process: "{metadata["process"]}"\\n',
        f'level: "{metadata["level"]}"\\n',
        f'tags: {json.dumps(metadata["tags"])}\\n',
        f'estimated_time_min: {metadata["estimated_time_min"]}\\n',
        "---\\n"
    ]
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }

def is_code_content(source_lines: List[str]) -> bool:
    """Determina si el contenido es código Python basándose en patrones"""
    content = ''.join(source_lines).strip()
    
    # Patrones que indican código Python
    code_patterns = [
        r'^import\s+\w+',  # import statements
        r'^from\s+\w+\s+import',  # from import
        r'^\w+\s*=\s*.+',  # assignments
        r'def\s+\w+\(',  # function definitions
        r'class\s+\w+',  # class definitions
        r'\.read_csv\(',  # pandas operations
        r'\.head\(\)',
        r'\.plot\(',
        r'print\(',
        r'plt\.',
        r'sns\.',
        r'pd\.',
        r'np\.',
    ]
    
    for pattern in code_patterns:
        if re.search(pattern, content, re.MULTILINE):
            return True
    
    # Si empieza con # pero tiene código después, es código
    lines = [l.strip() for l in source_lines if l.strip()]
    if lines and lines[0].startswith('#'):
        # Ver si hay código en las siguientes líneas
        for line in lines[1:]:
            if any(re.search(p, line) for p in code_patterns):
                return True
    
    return False

def is_markdown_content(source_lines: List[str]) -> bool:
    """Determina si el contenido es Markdown"""
    content = ''.join(source_lines).strip()
    
    # Patrones que indican Markdown
    markdown_patterns = [
        r'^#\s+[A-Z]',  # Headers estilo # Title
        r'^##\s+',  # ## Subtitles
        r'^\*\*',  # **bold**
        r'^-\s+',  # - list items
        r'^\d+\.\s+',  # 1. numbered lists
        r'^\>',  # > blockquotes
        r'^\|.+\|',  # | tables |
        r'---$',  # horizontal rules
    ]
    
    for pattern in markdown_patterns:
        if re.search(pattern, content, re.MULTILINE):
            return True
    
    return False

def fix_cell_type_smart(cell: Dict) -> tuple[Dict, bool]:
    """
    Corrige el tipo de celda basándose en el contenido real
    Retorna (cell_corregida, cambió)
    """
    cell_type = cell.get("cell_type", "")
    source = cell.get("source", [])
    if isinstance(source, str):
        source = [source]
    
    # Limpiar metadata incorrecto siempre
    metadata = cell.get("metadata", {})
    language = metadata.get("language")
    
    cambió = False
    
    # Determinar tipo correcto basándose en contenido
    has_code = is_code_content(source)
    has_markdown = is_markdown_content(source)
    
    # Decidir tipo correcto
    correct_type = None
    if has_code and not has_markdown:
        correct_type = "code"
    elif has_markdown and not has_code:
        correct_type = "markdown"
    elif cell_type == "code" and language == "markdown":
        correct_type = "markdown"
    elif cell_type == "markdown" and language == "python":
        correct_type = "code"
    
    # Aplicar corrección
    if correct_type and correct_type != cell_type:
        cell["cell_type"] = correct_type
        cambió = True
    
    # Limpiar metadata
    if correct_type == "markdown":
        cell["metadata"] = {}
        if language:
            cambió = True
    elif correct_type == "code":
        cell["metadata"] = {}
        if language:
            cambió = True
    
    return cell, cambió

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
    print(f"\\n🔍 Procesando: {notebook_path.name}")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    changed = False
    cells = notebook.get("cells", [])
    
    # 1. Corregir tipos de celda basándose en contenido
    for i, cell in enumerate(cells):
        original_type = cell.get("cell_type")
        fixed_cell, cell_changed = fix_cell_type_smart(cell)
        if cell_changed:
            cells[i] = fixed_cell
            changed = True
            new_type = fixed_cell.get("cell_type")
            print(f"   ✅ Celda {i+1}: {original_type} → {new_type}")
    
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
    print(f"\\n📊 Encontrados {len(notebook_files)} notebooks")
    
    # Excluir PLANTILLA y checkpoints
    notebook_files = [
        nb for nb in notebook_files 
        if "PLANTILLA" not in nb.name and ".ipynb_checkpoints" not in str(nb)
    ]
    
    fixed_count = 0
    for nb_path in sorted(notebook_files):
        if fix_notebook(nb_path):
            fixed_count += 1
    
    print(f"\\n✅ Proceso completado!")
    print(f"📝 Notebooks corregidos: {fixed_count}/{len(notebook_files)}")

if __name__ == "__main__":
    main()
