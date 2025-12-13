"""
Script para ejecutar todas las celdas del notebook OR-09 en orden
"""
import subprocess
import json

nb_path = "notebooks/50_optimization_or/OR-09-network_optimization.ipynb"

# Leer el notebook para obtener los cell IDs en orden
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Obtener IDs de celdas ejecutables (code cells)
code_cell_ids = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        cell_id = cell.get('id', f'cell_{i}')
        code_cell_ids.append((i+1, cell_id))

print(f"Encontradas {len(code_cell_ids)} celdas de código")
print("\nEjecutando en orden:")
for cell_num, cell_id in code_cell_ids[:15]:  # Ejecutar primeras 15
    print(f"  Celda {cell_num}: {cell_id}")
