# Supply Chain Data Notebooks

Repositorio de notebooks ejecutables para analítica de cadena de suministro y operaciones. Contiene datos sintéticos, cuadernos por especialidad y utilidades mínimas.

## Propósito

Esta es una **plataforma educativa ejecutable** para **líderes de supply chain** en todas sus especialidades. 
Aprende de forma práctica cómo se aplican:

- **Ingeniería de Datos**: Pipelines ETL, modelado dimensional, calidad de datos
- **Analítica Avanzada**: EDA, forecasting, análisis de riesgos, simulación
- **Inteligencia de Negocios**: KPIs, dashboards, análisis de desempeño
- **Arquitectura de Datos**: Modelado dimensional, data governance, integraciones
- **Inteligencia Artificial**: RAG, modelos predictivos, agentes generativos

Cada notebook es **100% ejecutable** con datos sintéticos reales del sector.

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

## Uso rápido: CLI Catalog

Navega y ejecuta notebooks desde la línea de comando sin comandos complejos:

```powershell
# Listar todos los notebooks
python -m scripts.catalog list

# Filtrar por especialidad
python -m scripts.catalog list --specialty "Data Science"
python -m scripts.catalog list --level Intro

# Buscar por palabra clave
python -m scripts.catalog search "inventory"

# Ver detalles de un notebook
python -m scripts.catalog show DS-01

# Ejecutar un notebook
python -m scripts.catalog run DS-01

# Ejecutar múltiples
python -m scripts.catalog run DS-01,DS-02,BA-01 --timeout 600
```

## Rutas de Aprendizaje (Learning Paths)

### 1. Para Líderes de Operaciones (Inicio rápido)
- **DS-01** (15 min): Entendimiento de datos de órdenes e inventarios
- **BA-01** (50 min): Cálculo de OTIF (métrica crítica de servicio)
- **OR-01** (55 min): Optimización de stock de seguridad

### 2. Para Analistas de Supply Chain (Intermedio)
- **DE-01** (30 min): Pipeline ETL desde sistemas transaccionales
- **DA-01** (60 min): Modelado dimensional de datos de cadena
- **DS-02** (40 min): Forecasting con detección de estacionalidad
- **BA-02-CTS** (45 min): Análisis de costos por ruta y cliente

### 3. Para Data Engineers / Architects (Avanzado)
- **DE-02** (45 min): Pipelines incrementales en tiempo real
- **OR-03** (60 min): Programación lineal para capacidad de centros
- **OR-04** (55 min): Inventario multi-echelon
- **RT-02** (50 min): Modelos predictivos de mantenimiento

### 4. Para líderes transformacionales (Full Journey)
- Seguir el orden de **Principiante → Intermedio → Avanzado** en cualquier especialidad
- Ver **Capstone** (CAP-01) como integración de todas las disciplinas

## Generar datos sintéticos

**Opción 1: Python (recomendado, cross-platform)**
```bash
# Generar 90 días (200 SKUs, todos los datos)
python data/synthetic_generators/generate_cli.py

# Generar 7 días (20 SKUs) para testing rápido
python data/synthetic_generators/generate_cli.py --fast

# Con semilla reproducible
python data/synthetic_generators/generate_cli.py --seed 42
```

**Opción 2: PowerShell (Windows)**
```powershell
pwsh data/synthetic_generators/generate_all.ps1
```

Los datos se guardan en `data/raw/`.

## Usar la CLI de Catálogo

Navega y ejecuta notebooks desde la línea de comando sin comandos complejos:

```bash
# Listar todos los notebooks
python -m scripts.catalog list

# Filtrar por especialidad
python -m scripts.catalog list --specialty "Data Science"
python -m scripts.catalog list --level Intro

# Buscar por palabra clave
python -m scripts.catalog search "inventory"

# Ver detalles de un notebook
python -m scripts.catalog show DS-01

# Ejecutar un notebook
python -m scripts.catalog run DS-01

# Ejecutar múltiples
python -m scripts.catalog run DS-01,DS-02,BA-01 --timeout 600
```

## Ejecutar notebooks (papermill directo)
```bash
papermill notebooks/30_data_science_ml/DS-01-eda.ipynb notebooks/30_data_science_ml/DS-01-eda.out.ipynb
```

## Smoke tests (validar que todo funciona)
```bash
python scripts/smoke_test_notebooks.py
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

## Índice de Notebooks (auto-generado)

Tabla generada desde `config/notebooks_index.yml` usando `python scripts/generate_notebook_catalog.py`.

<!-- NOTEBOOKS-TABLE:START -->
| ID | Título | Especialidad | Nivel | Notebook |
| --- | --- | --- | --- | --- |
| DE-01 | Ingesta batch desde WMS a DWH | Data Engineering | Intermediate | [DE-01-ingesta.ipynb](notebooks/10_data_engineering/DE-01-ingesta.ipynb) |
| DE-02 | Pipeline incremental de órdenes | Data Engineering | Intermediate | [DE-02-pipeline_incremental.ipynb](notebooks/10_data_engineering/DE-02-pipeline_incremental.ipynb) |
| DE-03 | ETL Básico con Pandas | Data Engineering | Intro | [DE-03-etl_basico.ipynb](notebooks/10_data_engineering/DE-03-etl_basico.ipynb) |
| DE-04 | Pipeline Streaming con Kafka | Data Engineering | Advanced | [DE-04-kafka_streaming.ipynb](notebooks/10_data_engineering/DE-04-kafka_streaming.ipynb) |
| DA-01 | Modelo dimensional para inventarios | Data Architecture | Intermediate | [DA-01-modelo_dimensional.ipynb](notebooks/20_data_architecture/DA-01-modelo_dimensional.ipynb) |
| DA-02 | Data Lake con Particiones | Data Architecture | Intermediate | [DA-02-data_lake_partitions.ipynb](notebooks/20_data_architecture/DA-02-data_lake_partitions.ipynb) |
| DS-01 | EDA de órdenes e inventarios | Data Science | Intro | [DS-01-eda.ipynb](notebooks/30_data_science_ml/DS-01-eda.ipynb) |
| DS-02 | Detección de estacionalidad en demanda | Data Science | Intermediate | [DS-02-estacionalidad.ipynb](notebooks/30_data_science_ml/DS-02-estacionalidad.ipynb) |
| DS-03 | Service level vs cost trade-off | Data Science | Intermediate | [DS-03-service_level_cost_tradeoff.ipynb](notebooks/30_data_science_ml/DS-03-service_level_cost_tradeoff.ipynb) |
| DS-04 | Last mile analytics | Data Science | Intermediate | [DS-04-last_mile_analytics.ipynb](notebooks/30_data_science_ml/DS-04-last_mile_analytics.ipynb) |
| DS-05 | Supply risk scenarios | Data Science | Intermediate | [DS-05-supply_risk_scenarios.ipynb](notebooks/30_data_science_ml/DS-05-supply_risk_scenarios.ipynb) |
| DS-06 | Forecast de Demanda con ARIMA | Data Science | Intermediate | [DS-06-forecast_arima.ipynb](notebooks/30_data_science_ml/DS-06-forecast_arima.ipynb) |
| DS-07 | ML Clasificación de Riesgo de Proveedores | Data Science | Advanced | [DS-07-supplier_risk_ml.ipynb](notebooks/30_data_science_ml/DS-07-supplier_risk_ml.ipynb) |
| BA-01 | Dashboard OTIF (On-Time In-Full) | Business Analytics | Intermediate | [BA-01-dashboard_otif.ipynb](notebooks/40_business_analytics_bi/BA-01-dashboard_otif.ipynb) |
| BA-02-CTS | Cost-to-Serve | Business Analytics | Intermediate | [BA-02-cost_to_serve.ipynb](notebooks/40_business_analytics_bi/BA-02-cost_to_serve.ipynb) |
| BA-02 | Planeación S&OP con escenarios de demanda | Business Analytics | Intermediate | [BA-02-sop_scenarios.ipynb](notebooks/40_business_analytics_bi/BA-02-sop_scenarios.ipynb) |
| BA-03 | Productividad de almacén | Business Analytics | Intermediate | [BA-03-warehouse_productivity.ipynb](notebooks/40_business_analytics_bi/BA-03-warehouse_productivity.ipynb) |
| BA-04 | Desempeño de proveedores | Business Analytics | Intermediate | [BA-04-supplier_performance.ipynb](notebooks/40_business_analytics_bi/BA-04-supplier_performance.ipynb) |
| BA-05 | Dashboard Ejecutivo de Supply Chain | Business Analytics | Intro | [BA-05-dashboard_ejecutivo.ipynb](notebooks/40_business_analytics_bi/BA-05-dashboard_ejecutivo.ipynb) |
| OR-01 | Cálculo de stock de seguridad | Optimization & OR | Intermediate | [OR-01-stock_seguridad.ipynb](notebooks/50_optimization_or/OR-01-stock_seguridad.ipynb) |
| OR-02-EOQ | Políticas de inventario (EOQ) | Optimization & OR | Intermediate | [OR-02-politicas_inventario.ipynb](notebooks/50_optimization_or/OR-02-politicas_inventario.ipynb) |
| OR-02-VRP | VRP con restricción de capacidad | Optimization & OR | Advanced | [OR-02-vrp_capacidad.ipynb](notebooks/50_optimization_or/OR-02-vrp_capacidad.ipynb) |
| OR-03 | Planeación de capacidad en CD y flota | Optimization & OR | Advanced | [OR-03-capacity_planning_dc_fleet.ipynb](notebooks/50_optimization_or/OR-03-capacity_planning_dc_fleet.ipynb) |
| OR-04 | Inventario multi‑echelon | Optimization & OR | Advanced | [OR-04-multi_echelon_inventory.ipynb](notebooks/50_optimization_or/OR-04-multi_echelon_inventory.ipynb) |
| OR-05 | Warehouse slotting | Optimization & OR | Intermediate | [OR-05-warehouse_slotting.ipynb](notebooks/50_optimization_or/OR-05-warehouse_slotting.ipynb) |
| OR-06 | Simulación de colas en andenes | Optimization & OR | Intermediate | [OR-06-dock_queue_simulation.ipynb](notebooks/50_optimization_or/OR-06-dock_queue_simulation.ipynb) |
| OR-07 | Cálculo de Stock de Seguridad | Optimization & OR | Intro | [OR-07-safety_stock_intro.ipynb](notebooks/50_optimization_or/OR-07-safety_stock_intro.ipynb) |
| OR-08 | Programación de Producción con PuLP | Optimization & OR | Intermediate | [OR-08-production_scheduling.ipynb](notebooks/50_optimization_or/OR-08-production_scheduling.ipynb) |
| OR-09 | Optimización de Red Logística Multiobjetivo | Optimization & OR | Advanced | [OR-09-network_optimization.ipynb](notebooks/50_optimization_or/OR-09-network_optimization.ipynb) |
| RT-01 | Simulación de stream de tracking | Realtime & IoT | Intro | [RT-01-stream_tracking.ipynb](notebooks/60_realtime_iot/RT-01-stream_tracking.ipynb) |
| RT-02 | Mantenimiento predictivo de flota | Realtime & IoT | Intermediate | [RT-02-fleet_predictive_maintenance.ipynb](notebooks/60_realtime_iot/RT-02-fleet_predictive_maintenance.ipynb) |
| RT-03 | Monitoreo de cadena de frío | Realtime & IoT | Intermediate | [RT-03-cold_chain_monitoring.ipynb](notebooks/60_realtime_iot/RT-03-cold_chain_monitoring.ipynb) |
| TR-01 | Análisis de transporte masivo con GTFS | Realtime & IoT | Intermediate | [TR-01-transporte_masivo.ipynb](notebooks/60_realtime_iot/TR-01-transporte_masivo.ipynb) |
| RT-04 | Visualización Básica de Sensores IoT | Realtime & IoT | Intro | [RT-04-iot_sensors_intro.ipynb](notebooks/60_realtime_iot/RT-04-iot_sensors_intro.ipynb) |
| GEN-01 | RAG para consultas de KPIs | AI Generativa | Intro | [GEN-01-rag_kpi.ipynb](notebooks/70_ai_gen_agents/GEN-01-rag_kpi.ipynb) |
| GEN-02 | LLM para Análisis de Texto en Supply Chain | AI Generativa | Intermediate | [GEN-02-llm_text_analysis.ipynb](notebooks/70_ai_gen_agents/GEN-02-llm_text_analysis.ipynb) |
| DG-01 | Perfilado de calidad de datos maestro | Data Governance | Intro | [DG-01-perfilado_calidad.ipynb](notebooks/80_governance_quality/DG-01-perfilado_calidad.ipynb) |
| CAP-01 | Torre de control | Capstone | Intro | [CAP-01-torre_control.ipynb](notebooks/90_capstone_end2end/CAP-01-torre_control.ipynb) |
<!-- NOTEBOOKS-TABLE:END -->

## Recursos

- [📚 Catálogo HTML Interactivo](docs/catalog.html) - Navega y filtra todos los notebooks
- [📖 Guía de Contribución](CONTRIBUTING.md) - Cómo crear nuevos notebooks
- [📋 Catálogo YAML](config/notebooks_index.yml) - Metadatos en formato máquina-legible
- [📚 Diccionario de datos](docs/data_dictionary.md)
- [🎯 Catálogo de casos](docs/use_case_catalog.md)

## Notas
- No se incluyen ni documentan contenidos fuera del árbol del repositorio.

## Créditos y Licencia
- Autor y mantenimiento: **lraigosov**.
- Licencia: Ver archivo `LICENSE` del repositorio.
