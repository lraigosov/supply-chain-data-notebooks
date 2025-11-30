# Supply Chain Data Notebooks

Proyecto realista para experimentar con notebooks ejecutables en supply chain y operaciones.

## Requisitos
- Python 3.11
- PowerShell (Windows)

## Setup
```powershell
# Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -U pip
pip install -e .[core,notebooks,or,iot,web,flow]
```

## Generar datos sintéticos
```powershell
pwsh data/synthetic_generators/generate_all.ps1
```

## Ejecutar un notebook de ejemplo
```powershell
papermill notebooks/30_data_science_ml/DS-01-eda.ipynb notebooks/30_data_science_ml/DS-01-eda.out.ipynb
```

## Estructura
Ver `bases/contenido.md` para el diseño general.
