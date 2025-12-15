# Catálogo de Casos de Uso

Descripción detallada de cada notebook implementado en el repositorio, organizado por especialidad. 
Basado en el contenido real de 40 notebooks ejecutables en `notebooks/` (+ 2 templates en 00_common/).

**Total de notebooks ejecutables:** 40 (9 intro, 24 intermediate, 7 advanced)

## 10_data_engineering/

### DE-01: Ingesta batch desde WMS a DWH
- **Nivel:** Intermedio
- **Tags:** etl, warehouse, inventory, python, sql
- **Datasets:** products.csv, orders.csv, inventory.csv
- **Tiempo estimado:** 45 min

### DE-02: Pipeline incremental de órdenes
- **Nivel:** Intermedio
- **Tags:** pipeline, incremental, orders
- **Datasets:** orders.csv

## 20_data_architecture/

### DA-01: Diseño de modelo dimensional para analítica de inventarios
- **Nivel:** Intermedio
- **Tags:** dimensional-modeling, star-schema, inventory, data-warehouse, analytics
- **Datasets:** inventory.csv, products.csv, locations.csv
- **Tiempo estimado:** 60 min

## 30_data_science_ml/

### DS-01: EDA de órdenes e inventarios
- **Nivel:** Intro
- **Tags:** eda, pandas, plot
- **Datasets:** orders.csv, inventory.csv
- **Tiempo estimado:** 40 min

### DS-02: Detección de estacionalidad en demanda
- **Nivel:** Intermedio
- **Tags:** seasonality, forecast, statsmodels
- **Datasets:** orders.csv

### DS-03: Service level vs cost trade-off
- **Nivel:** Intermedio
- **Tags:** service-level, cost, optimization
- **Datasets:** orders.csv, inventory.csv

### DS-04: Analítica de última milla
- **Nivel:** Intermedio
- **Tags:** last-mile, delivery, kpi
- **Datasets:** transport_events.csv

### DS-05: Escenarios de riesgo en suministro
- **Nivel:** Intermedio
- **Tags:** risk, supply, scenarios
- **Datasets:** Genera datos sintéticos internos

## 40_business_analytics_bi/

### BA-01: Dashboard de OTIF (On-Time In-Full) por cliente y región
- **Nivel:** Intermedio
- **Tags:** otif, kpi, delivery, dashboard, analytics, service-level
- **Datasets:** orders.csv, transport_events.csv, locations.csv
- **Tiempo estimado:** 50 min

### BA-02: Planeación S&OP con escenarios de demanda
- **Nivel:** Intermedio
- **Tags:** sop, scenarios, capacity, backlog, fill-rate, simulation
- **Datasets:** Genera datos sintéticos internos (3 familias, 12 semanas)
- **Tiempo estimado:** 45 min

### BA-02: Cost-to-Serve
- **Nivel:** Intermedio
- **Tags:** cost-to-serve, profitability
- **Datasets:** orders.csv, transport_events.csv

### BA-03: Productividad de almacén
- **Nivel:** Intermedio
- **Tags:** warehouse, productivity, kpi
- **Datasets:** inventory.csv, orders.csv

### BA-04: Desempeño de proveedores
- **Nivel:** Intermedio
- **Tags:** supplier, kpi, reliability
- **Datasets:** orders.csv

## 50_optimization_or/

### OR-01: Cálculo de stock de seguridad con fórmulas clásicas
- **Nivel:** Intermedio
- **Tags:** safety-stock, inventory, optimization, service-level, statistics
- **Datasets:** orders.csv, products.csv
- **Tiempo estimado:** 55 min

### OR-02: Políticas de inventario (EOQ)
- **Nivel:** Intermedio
- **Tags:** inventory, eoq, optimization
- **Datasets:** Genera datos sintéticos internos
- **Tiempo estimado:** 50 min

### OR-02: Problema de ruteo de vehículos (VRP) con restricción de capacidad
- **Nivel:** Avanzado
- **Tags:** vrp, routing, optimization, pulp, capacity, last-mile
- **Datasets:** Genera datos sintéticos internos
- **Tiempo estimado:** 65 min

### OR-03: Planeación de capacidad en CD y flota
- **Nivel:** Avanzado
- **Tags:** capacity, warehouse, fleet, linear-programming, pulp
- **Datasets:** Genera datos sintéticos internos (20 días, capacidad CD/flota)
- **Tiempo estimado:** 60 min

### OR-04: Inventario multi‑echelon
- **Nivel:** Avanzado
- **Tags:** multi-echelon, inventory
- **Datasets:** Genera datos sintéticos internos

### OR-05: Warehouse slotting
- **Nivel:** Intermedio
- **Tags:** slotting, warehouse, layout
- **Datasets:** Genera datos sintéticos internos

### OR-06: Simulación de colas en andenes
- **Nivel:** Intermedio
- **Tags:** queueing, simulation, mmc
- **Datasets:** Genera datos sintéticos internos

## 60_realtime_iot/

### RT-01: Simulación de stream de tracking GPS
- **Nivel:** Intro
- **Tags:** stream, tracking, iot, async, geofencing
- **Datasets:** transport_events.csv
- **Tiempo estimado:** 40 min

### RT-02: Mantenimiento predictivo de flota
- **Nivel:** Intermedio
- **Tags:** predictive, maintenance, classification
- **Datasets:** Genera datos sintéticos internos

### RT-03: Monitoreo de cadena de frío
- **Nivel:** Intermedio
- **Tags:** cold-chain, temperature, alerts
- **Datasets:** Genera series de temperatura sintéticas

### TR-01: Análisis de transporte masivo con GTFS
- **Nivel:** Intermedio
- **Tags:** gtfs, transit, geospatial, geopandas, folium
- **Datasets:** gtfs_local.zip, gtfs_sample.zip (archivos GTFS estándar en `data/raw/`)
- **Tiempo estimado:** 55 min

### OR-07: Cálculo de Stock de Seguridad (Intro)
- **Nivel:** Intro
- **Tags:** inventory, safety-stock, optimization, operations, demand-variability
- **Datasets:** orders.csv, products.csv, inventory.csv
- **Tiempo estimado:** 30 min
- **Propósito:** Introducción simplificada al cálculo de stock de seguridad para líderes operacionales.

### OR-08: Programación de Producción con PuLP
- **Nivel:** Intermediate
- **Tags:** optimization, pulp, linear-programming, production, scheduling
- **Datasets:** orders.csv, products.csv
- **Tiempo estimado:** 50 min
- **Propósito:** Programar producción minimizando makespan, cambios de setup, tardíos.

### OR-09: Optimización de Red Logística Multiobjetivo
- **Nivel:** Advanced
- **Tags:** optimization, network-design, ortools, multi-objective, facility-location
- **Datasets:** locations.csv, orders.csv
- **Tiempo estimado:** 70 min
- **Propósito:** Decidir ubicación óptima de plantas y DCs balanceando costo, cobertura, resiliencia.

## 60_realtime_iot/ (5 notebooks)

### RT-01: Simulación de stream de tracking GPS
- **Nivel:** Intro
- **Tags:** stream, tracking
- **Datasets:** transport_events.csv

### RT-02: Mantenimiento predictivo de flota
- **Nivel:** Intermediate
- **Tags:** predictive, maintenance, classification
- **Datasets:** Genera datos sintéticos internos

### RT-03: Monitoreo de cadena de frío
- **Nivel:** Intermediate
- **Tags:** cold-chain, temperature, alerts
- **Datasets:** Genera series de temperatura sintéticas

### RT-04: Visualización Básica de Sensores IoT
- **Nivel:** Intro
- **Tags:** iot, sensors, realtime, visualization, monitoring
- **Datasets:** transport_events.csv, locations.csv
- **Tiempo estimado:** 30 min
- **Propósito:** Introducción a lectura y visualización de datos IoT en tiempo real.

### TR-01: Análisis de transporte masivo con GTFS
- **Nivel:** Intermediate
- **Tags:** gtfs, transit, geospatial
- **Datasets:** gtfs_local.zip, gtfs_sample.zip (archivos GTFS estándar en `data/raw/`)
- **Tiempo estimado:** 55 min

## 70_ai_gen_agents/ (2 notebooks)

### GEN-01: RAG para consultas de KPIs
- **Nivel:** Intro
- **Tags:** rag, kpi
- **Datasets:** Genera corpus de KPIs internamente
- **Propósito:** Sistema que responde preguntas sobre KPIs usando RAG (Retrieval Augmented Generation).

### GEN-02: LLM para Análisis de Texto en Supply Chain
- **Nivel:** Intermediate
- **Tags:** llm, openai, nlp, text-analysis, ai, sentiment
- **Datasets:** orders.csv, products.csv (genera reclamaciones sintéticas)
- **Tiempo estimado:** 45 min
- **Propósito:** Clasificar, categorizar y analizar sentimiento en quejas/reclamaciones. Solicita Gemini API key interactivamente (opcional, incluye modo demo).

## 80_governance_quality/ (1 notebook)

### DG-01: Perfilado de calidad de datos maestro
- **Nivel:** Intermediate
- **Tags:** quality, profiling, data-governance, validation
- **Datasets:** products.csv

## 90_capstone_end2end/ (1 notebook)

### CAP-01: Torre de control (dashboard integrado)
- **Nivel:** Intermediate
- **Tags:** capstone, dashboard, kpi, integration
- **Datasets:** orders.csv, inventory.csv, transport_events.csv

## 99_utilidades/ (2 notebooks)

### AP-01: Aplicar Todo DataFrame
- **Nivel:** Intermediate
- **Tags:** pandas, dataframe, vectorization, performance, optimization, etl
- **Datasets:** Genera ejemplos sintéticos
- **Tiempo estimado:** 40 min
- **Propósito:** Técnicas de procesamiento vectorizado de DataFrames para mejorar performance 10-100x vs bucles/apply tradicionales.

### SI-09: Flujo Si9 - Automatización S&OP End-to-End
- **Nivel:** Advanced
- **Tags:** sop, pipeline, automation, machine-learning, workflow, sklearn
- **Datasets:** Genera ejemplos sintéticos
- **Tiempo estimado:** 50 min
- **Propósito:** Pipeline automatizado end-to-end para procesos S&OP con ML, reduciendo ciclo de 20 a 5 días.

---

## Resumen por Nivel

| Nivel | Cantidad | Descripción |
|-------|----------|-------------|
| **Intro** | 9 | 15-30 min, conceptos fundamentales, sin prerequisitos |
| **Intermediate** | 24 | 30-60 min, aplicaciones prácticas, algunos prerequisitos |
| **Advanced** | 7 | 60+ min, casos complejos de producción, teoría avanzada |

## Resumen por Especialidad

| Especialidad | Notebooks | Propósito |
|--------------|-----------|----------|
| Data Engineering | 4 | ETL, pipelines, streaming |
| Data Architecture | 2 | Modelado, data lakes, governance |
| Data Science/ML | 7 | EDA, forecasting, classification, risk |
| Business Analytics | 6 | KPIs, dashboards, S&OP |
| Optimization/OR | 10 | Inventario, routing, scheduling, capacity |
| Realtime/IoT | 5 | Streaming, tracking, sensors, GTFS |
| AI Generativa | 2 | RAG, LLM, text analysis |
| Data Governance | 1 | Calidad, profiling |
| Capstone | 1 | Integración end-to-end |
| Utilidades | 2 | Tutoriales, fundamentos |
| **TOTAL** | **40** | **Plataforma educativa ejecutable** |

---

**Referencia**: `config/notebooks_index.yml`
**Última actualización**: Diciembre 2025
