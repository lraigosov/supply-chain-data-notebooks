# Supply Chain Data Notebooks

Repositorio de notebooks ejecutables para analítica de cadena de suministro y operaciones. Contiene datos sintéticos, cuadernos por especialidad y utilidades mínimas.

## Estado actual
- Notebooks organizados en subcarpetas por temática (Engineering, Architecture, Data Science, BI, OR, IoT, GenAI, Governance, Capstone, Utilidades).
- Datos sintéticos disponibles en `data/raw/` y salidas en `data/processed/`.
- Ejecución de notebooks verificada con `papermill` en entorno virtual.

## Requisitos
- Python 3.10 (entorno virtual en `.venv`)
- PowerShell (Windows)

## Setup
```powershell
# Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias base
pip install -U pip
pip install pandas numpy matplotlib seaborn plotly scipy pyyaml pyarrow pulp papermill
```

## Generar datos sintéticos
```powershell
pwsh data/synthetic_generators/generate_all.ps1
```

## Ejecutar notebooks (papermill)
```powershell
# Usando papermill del venv
F:\GitHub\supply-chain-data-notebooks\.venv\Scripts\papermill.exe \
	"notebooks/30_data_science_ml/DS-01-eda.ipynb" \
	"notebooks/30_data_science_ml/DS-01-eda.out.ipynb"
```

## Estructura del proyecto
```
.
├── config/
│   └── notebooks_index.yml
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic_generators/
├── docs/
│   ├── data_dictionary.md
│   └── use_case_catalog.md
├── notebooks/
│   ├── 10_data_engineering/
│   ├── 20_data_architecture/
│   ├── 30_data_science_ml/
│   ├── 40_business_analytics_bi/
│   ├── 50_optimization_or/
│   ├── 60_realtime_iot/
│   ├── 70_ai_gen_agents/
│   ├── 80_governance_quality/
│   ├── 90_capstone_end2end/
│   └── 99_utilidades/
├── src/
│   └── utils/
├── tests/
│   ├── data_tests/
│   └── unit_tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Recursos
- Catálogo de notebooks: `config/notebooks_index.yml`
- Diccionario de datos: `docs/data_dictionary.md`
- Catálogo de casos: `docs/use_case_catalog.md`

## Notas
- `bases/` existe en el repositorio; no está ignorada por Git.
- No se incluyen ni documentan contenidos fuera del árbol del repositorio.

## Licencia
Uso educativo y demostrativo.
