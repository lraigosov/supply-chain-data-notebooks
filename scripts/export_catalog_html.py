"""
Exportar catálogo de notebooks a HTML interactivo.

Genera una página HTML con filtros, búsqueda y navegación fácil.

Uso:
  python scripts/export_catalog_html.py
  python scripts/export_catalog_html.py --output /custom/path/catalog.html
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "config" / "notebooks_index.yml"
DEFAULT_OUTPUT = ROOT / "docs" / "catalog.html"


def load_index() -> list[dict]:
    """Load notebooks from index."""
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("notebooks", [])


def group_by_specialty(notebooks: list[dict]) -> dict[str, list[dict]]:
    """Group notebooks by specialty."""
    grouped = {}
    for nb in notebooks:
        spec = nb.get("specialty", "Other")
        if spec not in grouped:
            grouped[spec] = []
        grouped[spec].append(nb)
    return grouped


def generate_html(notebooks: list[dict]) -> str:
    """Generate HTML catalog."""
    grouped = group_by_specialty(notebooks)
    
    # Build table rows
    rows = []
    for nb in notebooks:
        nb_id = nb.get("id", "")
        title = nb.get("title", "")
        specialty = nb.get("specialty", "")
        level = nb.get("level", "")
        path = nb.get("path", "")
        tags = nb.get("tags", [])
        duration = nb.get("estimated_time_min", "")
        datasets = nb.get("dataset_deps", [])

        level_badge = f'<span class="badge badge-{level.lower()}">{level}</span>'
        tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in tags])
        datasets_html = ", ".join(datasets) if datasets else "-"
        duration_html = f"{duration}m" if duration else "-"
        path_html = f'<a href="{path}" target="_blank">{Path(path).name}</a>'

        row = f"""
        <tr data-specialty="{specialty}" data-level="{level}" data-tags="{','.join(tags)}">
            <td class="id"><strong>{nb_id}</strong></td>
            <td class="title">{title}</td>
            <td class="specialty"><small>{specialty}</small></td>
            <td class="level">{level_badge}</td>
            <td class="duration"><small>{duration_html}</small></td>
            <td class="datasets"><small>{datasets_html}</small></td>
            <td class="tags"><small>{tags_html}</small></td>
            <td class="notebook">{path_html}</td>
        </tr>
        """
        rows.append(row)

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supply Chain Notebooks Catalog</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}
        
        .controls {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .control-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .control-group label {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
            font-size: 0.9em;
        }}
        
        input[type="text"],
        select {{
            padding: 10px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.95em;
            background: white;
        }}
        
        input[type="text"]:focus,
        select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
            color: white;
        }}
        
        .badge-intro {{
            background: #10b981;
        }}
        
        .badge-intermediate {{
            background: #f59e0b;
        }}
        
        .badge-advanced {{
            background: #ef4444;
        }}
        
        .tag {{
            display: inline-block;
            background: #e0e7ff;
            color: #667eea;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            margin-right: 4px;
        }}
        
        .table-wrapper {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}
        
        thead {{
            background: #f3f4f6;
            border-bottom: 2px solid #e5e7eb;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #374151;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        tbody tr:hover {{
            background: #f9fafb;
        }}
        
        .id {{
            font-family: monospace;
            color: #667eea;
            font-weight: 600;
            width: 80px;
        }}
        
        .title {{
            font-weight: 500;
            color: #1f2937;
            max-width: 250px;
        }}
        
        .notebook a {{
            color: #667eea;
            text-decoration: none;
            font-family: monospace;
            font-size: 0.85em;
        }}
        
        .notebook a:hover {{
            text-decoration: underline;
        }}
        
        .hidden {{
            display: none;
        }}
        
        footer {{
            background: #f3f4f6;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e5e7eb;
        }}
        
        .stats {{
            padding: 30px;
            background: white;
            text-align: center;
            border-top: 1px solid #e0e0e0;
        }}
        
        .stat {{
            display: inline-block;
            margin: 0 30px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Supply Chain Data Notebooks</h1>
            <p>Plataforma ejecutable para líderes de supply chain</p>
        </header>
        
        <div class="controls">
            <div class="control-group">
                <label>Buscar:</label>
                <input type="text" id="search" placeholder="Título, ID, tag...">
            </div>
            <div class="control-group">
                <label>Especialidad:</label>
                <select id="specialty">
                    <option value="">Todas</option>
                    {"".join([f'<option value="{spec}">{spec}</option>' for spec in sorted(group_by_specialty(notebooks).keys())])}
                </select>
            </div>
            <div class="control-group">
                <label>Nivel:</label>
                <select id="level">
                    <option value="">Todos</option>
                    <option value="Intro">Intro</option>
                    <option value="Intermediate">Intermedio</option>
                    <option value="Advanced">Avanzado</option>
                </select>
            </div>
        </div>
        
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Título</th>
                        <th>Especialidad</th>
                        <th>Nivel</th>
                        <th>Duración</th>
                        <th>Datasets</th>
                        <th>Tags</th>
                        <th>Notebook</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(notebooks)}</div>
                <div class="stat-label">Notebooks</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(set(nb.get('specialty') for nb in notebooks))}</div>
                <div class="stat-label">Especialidades</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(set(tag for nb in notebooks for tag in nb.get('tags', [])))}</div>
                <div class="stat-label">Tags únicos</div>
            </div>
        </div>
        
        <footer>
            Generado automáticamente | <a href="https://github.com/lraigosov/supply-chain-data-notebooks" style="color: #667eea;">GitHub</a>
        </footer>
    </div>
    
    <script>
        const searchInput = document.getElementById("search");
        const specialtySelect = document.getElementById("specialty");
        const levelSelect = document.getElementById("level");
        const tableBody = document.getElementById("table-body");
        const rows = Array.from(tableBody.querySelectorAll("tr"));
        
        function filterRows() {{
            const searchTerm = searchInput.value.toLowerCase();
            const specialty = specialtySelect.value;
            const level = levelSelect.value;
            
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                const rowSpecialty = row.dataset.specialty;
                const rowLevel = row.dataset.level;
                const rowTags = row.dataset.tags.split(",");
                
                const matchSearch = !searchTerm || text.includes(searchTerm) || rowTags.some(tag => tag.toLowerCase().includes(searchTerm));
                const matchSpecialty = !specialty || rowSpecialty === specialty;
                const matchLevel = !level || rowLevel === level;
                
                row.classList.toggle("hidden", !(matchSearch && matchSpecialty && matchLevel));
            }});
        }}
        
        searchInput.addEventListener("input", filterRows);
        specialtySelect.addEventListener("change", filterRows);
        levelSelect.addEventListener("change", filterRows);
    </script>
</body>
</html>
    """
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description="Export notebook catalog to HTML")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output HTML file (default: {DEFAULT_OUTPUT})"
    )
    args = parser.parse_args()
    
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    notebooks = load_index()
    html = generate_html(notebooks)
    output_path.write_text(html, encoding="utf-8")
    
    print(f"✅ Catálogo exportado a: {output_path}")
    print(f"   Abre en navegador: file://{output_path.absolute()}")


if __name__ == "__main__":
    main()
