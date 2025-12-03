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

## Índice de Notebooks

### 10_data_engineering/
- `DE-01`: [Ingesta batch desde WMS a DWH](notebooks/10_data_engineering/DE-01-ingesta.ipynb)
- `DE-02`: [Pipeline incremental de órdenes](notebooks/10_data_engineering/DE-02-pipeline_incremental.ipynb)

### 20_data_architecture/
- `DA-01`: [Modelo dimensional para inventarios](notebooks/20_data_architecture/DA-01-modelo_dimensional.ipynb)

### 30_data_science_ml/
- `DS-01`: [EDA de órdenes e inventarios](notebooks/30_data_science_ml/DS-01-eda.ipynb)
- `DS-02`: [Detección de estacionalidad en demanda](notebooks/30_data_science_ml/DS-02-estacionalidad.ipynb)

### 40_business_analytics_bi/
- `BA-01`: [Dashboard OTIF (On-Time In-Full)](notebooks/40_business_analytics_bi/BA-01-dashboard_otif.ipynb)
- `BA-02`: [Planeación S&OP con escenarios de demanda](notebooks/40_business_analytics_bi/BA-02-sop_scenarios.ipynb)

### 50_optimization_or/
- `OR-01`: [Cálculo de stock de seguridad](notebooks/50_optimization_or/OR-01-stock_seguridad.ipynb)
- `OR-02`: [Políticas de inventario (EOQ)](notebooks/50_optimization_or/OR-02-politicas_inventario.ipynb)
- `OR-02`: [VRP con restricción de capacidad](notebooks/50_optimization_or/OR-02-vrp_capacidad.ipynb)
- `OR-03`: [Planeación de capacidad en CD y flota](notebooks/50_optimization_or/OR-03-capacity_planning_dc_fleet.ipynb)

### 60_realtime_iot/
- `RT-01`: [Simulación de stream de tracking GPS](notebooks/60_realtime_iot/RT-01-stream_tracking.ipynb)
- `TR-01`: [Análisis de transporte masivo con GTFS](notebooks/60_realtime_iot/TR-01-transporte_masivo.ipynb)

### 70_ai_gen_agents/
- `GEN-01`: [RAG para consultas de KPIs](notebooks/70_ai_gen_agents/GEN-01-rag_kpi.ipynb)

### 80_governance_quality/
- `DG-01`: [Perfilado de calidad de datos maestro](notebooks/80_governance_quality/DG-01-perfilado_calidad.ipynb)

### 90_capstone_end2end/
- `CAP-01`: [Torre de control](notebooks/90_capstone_end2end/CAP-01-torre_control.ipynb)

### 99_utilidades/
- `AP-01`: [Apply en DataFrames - Tutorial pandas](notebooks/99_utilidades/AP-01-aplicar_todo_dataframe.ipynb)
- `SI-09`: [Flujo ML end-to-end con scikit-learn](notebooks/99_utilidades/SI-09-flujo_si9.ipynb)

## Recursos
- Catálogo de notebooks: `config/notebooks_index.yml`
- Diccionario de datos: `docs/data_dictionary.md`
- Catálogo de casos: `docs/use_case_catalog.md`

## Notas
- `bases/` existe en el repositorio; no está ignorada por Git.
- No se incluyen ni documentan contenidos fuera del árbol del repositorio.

## Créditos y Licencia
- Autor y mantenimiento: **lraigosov**.
- Contenidos (notebooks y documentación): **CC BY 4.0** — requiere atribución al autor. Ver `LICENSE`.
- Código auxiliar (cuando aplique): licencia permisiva indicada en metadatos del proyecto.
- Desarrollo asistido por **GitHub Copilot Free** (code completions, refactoring, documentation).
- Análisis automatizado con **GitHub Copilot Actions** (code review, security scanning).
