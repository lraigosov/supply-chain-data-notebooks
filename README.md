# Supply Chain Data Notebooks

Repositorio de notebooks ejecutables para analítica de cadena de suministro y operaciones. Contiene datos sintéticos, cuadernos por especialidad y utilidades mínimas.

## Estado actual
- Notebooks organizados en subcarpetas por temática (Engineering, Architecture, Data Science, BI, OR, IoT, GenAI, Governance, Capstone, Utilidades).
- Datos sintéticos disponibles en `data/raw/` y salidas en `data/processed/`.
- Ejecución de notebooks verificada con `papermill` en entorno virtual.

## Requisitos
- Python 3.10+
- PowerShell (Windows)

## Setup
```powershell
# Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias del proyecto (opcional editable)
pip install -U pip
pip install -e .[core,notebooks,or,iot,web,flow]
```

## Generar datos sintéticos
```powershell
pwsh data/synthetic_generators/generate_all.ps1
```

## Ejecutar notebooks (papermill)
```powershell
papermill notebooks/30_data_science_ml/DS-01-eda.ipynb notebooks/30_data_science_ml/DS-01-eda.out.ipynb
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
│   ├── 00_common/
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
├── scripts/
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
- `DS-03`: [Service level vs cost trade-off](notebooks/30_data_science_ml/DS-03-service_level_cost_tradeoff.ipynb)
- `DS-04`: [Last mile analytics](notebooks/30_data_science_ml/DS-04-last_mile_analytics.ipynb)
- `DS-05`: [Supply risk scenarios](notebooks/30_data_science_ml/DS-05-supply_risk_scenarios.ipynb)

### 40_business_analytics_bi/
- `BA-01`: [Dashboard OTIF (On-Time In-Full)](notebooks/40_business_analytics_bi/BA-01-dashboard_otif.ipynb)
- `BA-02`: [Cost-to-Serve](notebooks/40_business_analytics_bi/BA-02-cost_to_serve.ipynb)
- `BA-02`: [Planeación S&OP con escenarios de demanda](notebooks/40_business_analytics_bi/BA-02-sop_scenarios.ipynb)
- `BA-03`: [Productividad de almacén](notebooks/40_business_analytics_bi/BA-03-warehouse_productivity.ipynb)
- `BA-04`: [Desempeño de proveedores](notebooks/40_business_analytics_bi/BA-04-supplier_performance.ipynb)

### 50_optimization_or/
- `OR-01`: [Cálculo de stock de seguridad](notebooks/50_optimization_or/OR-01-stock_seguridad.ipynb)
- `OR-02`: [Políticas de inventario (EOQ)](notebooks/50_optimization_or/OR-02-politicas_inventario.ipynb)
- `OR-02`: [VRP con restricción de capacidad](notebooks/50_optimization_or/OR-02-vrp_capacidad.ipynb)
- `OR-03`: [Planeación de capacidad en CD y flota](notebooks/50_optimization_or/OR-03-capacity_planning_dc_fleet.ipynb)
- `OR-04`: [Inventario multi‑echelon](notebooks/50_optimization_or/OR-04-multi_echelon_inventory.ipynb)
- `OR-05`: [Warehouse slotting](notebooks/50_optimization_or/OR-05-warehouse_slotting.ipynb)
- `OR-06`: [Simulación de colas en andenes](notebooks/50_optimization_or/OR-06-dock_queue_simulation.ipynb)

### 60_realtime_iot/
- `RT-01`: [Simulación de stream de tracking GPS](notebooks/60_realtime_iot/RT-01-stream_tracking.ipynb)
- `RT-02`: [Mantenimiento predictivo de flota](notebooks/60_realtime_iot/RT-02-fleet_predictive_maintenance.ipynb)
- `RT-03`: [Monitoreo de cadena de frío](notebooks/60_realtime_iot/RT-03-cold_chain_monitoring.ipynb)
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
- No se incluyen ni documentan contenidos fuera del árbol del repositorio.

## Créditos y Licencia
- Autor y mantenimiento: **lraigosov**.
- Licencia: Ver archivo `LICENSE` del repositorio.
