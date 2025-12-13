#!/usr/bin/env python3
"""
Script para actualizar las secciones de navegación en todos los notebooks
a un formato markdown legible y consistente.
"""
import json
import re
from pathlib import Path
import yaml


def load_notebooks_index(config_path: Path) -> list:
    """Carga el índice de notebooks desde el YAML."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config['notebooks']


def get_navigation_info(notebooks: list, notebook_path: str) -> tuple:
    """Obtiene la información de navegación para un notebook dado."""
    # Normalizar el path para comparación
    normalized_path = notebook_path.replace('\\', '/')
    
    for i, nb in enumerate(notebooks):
        if normalized_path.endswith(nb['path']):
            prev_nb = notebooks[i - 1] if i > 0 else None
            next_nb = notebooks[i + 1] if i < len(notebooks) - 1 else None
            return prev_nb, next_nb
    
    return None, None


def create_navigation_markdown(prev_nb: dict, next_nb: dict, current_folder: str) -> str:
    """Crea el markdown de navegación con el formato mejorado."""
    lines = ["---\n", "\n", "## 📚 Navegación\n", "\n"]
    
    # Enlace anterior
    if prev_nb:
        prev_filename = Path(prev_nb['path']).name
        prev_folder = Path(prev_nb['path']).parent.name
        prev_path = f"../{prev_folder}/{prev_filename}"
        lines.append(f"- Anterior: [{prev_filename}]({prev_path})\n")
    
    # Enlaces fijos
    lines.append("- Índice del proyecto: [README.md](../../README.md)\n")
    lines.append("- Catálogo de notebooks: [notebooks_index.yml](../../config/notebooks_index.yml)\n")
    
    # Enlace siguiente
    if next_nb:
        next_filename = Path(next_nb['path']).name
        next_folder = Path(next_nb['path']).parent.name
        
        # Si está en la misma carpeta, usar path relativo simple
        if next_folder == current_folder:
            next_path = f"../{next_folder}/{next_filename}"
        else:
            next_path = f"../{next_folder}/{next_filename}"
        
        lines.append(f"- Siguiente: [{next_filename}]({next_path})\n")
    
    return "".join(lines)


def find_navigation_cell(notebook_data: dict) -> int:
    """Encuentra el índice de la celda de navegación en el notebook."""
    cells = notebook_data.get('cells', [])
    
    for i, cell in enumerate(cells):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            
            # Buscar patrones que indiquen una celda de navegación
            if any(pattern in source for pattern in [
                '← Anterior',
                'Anterior:',
                '📚 Navegación',
                '📑 Índice',
                '📋 Catálogo',
                'Siguiente →'
            ]):
                return i
    
    return -1


def update_notebook_navigation(notebook_path: Path, notebooks_index: list):
    """Actualiza la navegación de un notebook específico."""
    
    # Cargar el notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Obtener información de navegación
    prev_nb, next_nb = get_navigation_info(notebooks_index, str(notebook_path))
    
    if prev_nb is None and next_nb is None:
        print(f"⚠️  {notebook_path.name}: No encontrado en el índice, saltando...")
        return False
    
    # Buscar la celda de navegación
    nav_cell_index = find_navigation_cell(notebook_data)
    
    if nav_cell_index == -1:
        print(f"⚠️  {notebook_path.name}: No se encontró celda de navegación, saltando...")
        return False
    
    # Crear el nuevo markdown de navegación
    current_folder = notebook_path.parent.name
    new_markdown = create_navigation_markdown(prev_nb, next_nb, current_folder)
    
    # Actualizar la celda
    notebook_data['cells'][nav_cell_index]['source'] = new_markdown.split('\n')
    
    # Guardar el notebook actualizado
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, ensure_ascii=False, indent=1)
    
    print(f"✅ {notebook_path.name}: Navegación actualizada")
    return True


def main():
    """Función principal."""
    # Rutas base
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / 'config' / 'notebooks_index.yml'
    notebooks_dir = repo_root / 'notebooks'
    
    # Cargar el índice
    print("📖 Cargando índice de notebooks...")
    notebooks_index = load_notebooks_index(config_path)
    print(f"   Encontrados {len(notebooks_index)} notebooks en el índice")
    
    # Buscar todos los notebooks (excepto plantillas)
    print("\n🔍 Buscando notebooks...")
    notebook_files = []
    for folder in notebooks_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('00_common'):
            for nb_file in folder.glob('*.ipynb'):
                if not nb_file.name.startswith('.'):
                    notebook_files.append(nb_file)
    
    print(f"   Encontrados {len(notebook_files)} archivos .ipynb")
    
    # Actualizar cada notebook
    print("\n🔄 Actualizando navegación...\n")
    updated = 0
    skipped = 0
    
    for nb_path in sorted(notebook_files):
        if update_notebook_navigation(nb_path, notebooks_index):
            updated += 1
        else:
            skipped += 1
    
    # Resumen
    print(f"\n{'='*60}")
    print(f"✨ Proceso completado:")
    print(f"   • Notebooks actualizados: {updated}")
    print(f"   • Notebooks saltados: {skipped}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
