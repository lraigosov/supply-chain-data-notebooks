#!/usr/bin/env python
"""
Script de auditoría: verificar estado de contextos de negocio en notebooks.
"""

import json
from pathlib import Path
from typing import Dict

def audit_context(notebook_path: Path) -> Dict:
    """Analizar estado del contexto de negocio en un notebook."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        notebook_id = notebook_path.stem.split('-')[0:2]
        notebook_id = f"{notebook_id[0]}-{notebook_id[1]}" if len(notebook_id) >= 2 else notebook_id[0]
        
        # Buscar sección de contexto
        context_found = False
        context_has_todo = False
        context_length = 0
        context_text = ""
        
        for cell in content.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                source_text = ''.join(source) if isinstance(source, list) else source
                
                if 'Contexto de Negocio' in source_text or 'contexto de negocio' in source_text.lower():
                    context_found = True
                    context_text = source_text
                    context_length = len(source_text)
                    if 'TODO' in source_text:
                        context_has_todo = True
                    break
        
        return {
            'id': notebook_id,
            'path': str(notebook_path.relative_to(Path(__file__).parent.parent)),
            'has_context': context_found,
            'has_todo': context_has_todo,
            'length': context_length,
            'status': 'DONE' if (context_found and not context_has_todo and context_length > 500) else 'PENDING' if not context_found else 'PARTIAL'
        }
    except Exception as e:
        return {'id': '??', 'path': str(notebook_path), 'error': str(e), 'status': 'ERROR'}

def main():
    notebooks_root = Path(__file__).parent.parent / "notebooks"
    notebook_files = sorted(notebooks_root.glob("**/[!TEMPLATE]*.ipynb"))
    notebook_files = [f for f in notebook_files if "PLANTILLA" not in f.name and "TEMPLATE" not in f.name]
    
    print(f"\n📊 Auditoría de contextos en {len(notebook_files)} notebooks\n")
    
    results = []
    for notebook_path in notebook_files:
        audit = audit_context(notebook_path)
        results.append(audit)
        
        icon = '✅' if audit['status'] == 'DONE' else '⚠️' if audit['status'] == 'PARTIAL' else '❌'
        print(f"{icon} {audit['id']:12} | {audit['status']:8} | {audit['length']:5} chars | {audit['path']}")
    
    # Resumen
    print(f"\n📈 Resumen:")
    done = sum(1 for r in results if r['status'] == 'DONE')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    pending = sum(1 for r in results if r['status'] == 'PENDING')
    error = sum(1 for r in results if r['status'] == 'ERROR')
    
    print(f"  ✅ Completos: {done}")
    print(f"  ⚠️  Parciales: {partial}")
    print(f"  ❌ Pendientes: {pending}")
    print(f"  🔥 Errores: {error}")
    print(f"  📊 Total: {len(results)}")
    print()

if __name__ == "__main__":
    main()
