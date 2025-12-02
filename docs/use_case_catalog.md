# Catálogo de Casos de Uso

Catálogo de los notebooks presentes en el repositorio, organizados por especialidad. Se basa en el contenido real de `notebooks/`.

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

## 40_business_analytics_bi/

### BA-01: Dashboard de OTIF (On-Time In-Full) por cliente y región
- **Nivel:** Intermedio
- **Tags:** otif, kpi, delivery, dashboard, analytics, service-level
- **Datasets:** orders.csv, transport_events.csv, locations.csv
- **Tiempo estimado:** 50 min

## 50_optimization_or/

### OR-01: Cálculo de stock de seguridad con fórmulas clásicas
- **Nivel:** Intermedio
- **Tags:** safety-stock, inventory, optimization, service-level, statistics
- **Datasets:** orders.csv, products.csv
- **Tiempo estimado:** 55 min

### OR-02: Políticas de inventario (EOQ)
- **Nivel:** Intermedio
- **Tags:** inventory, eoq, optimization
- **Datasets:** orders.csv, products.csv

### OR-02: Problema de ruteo de vehículos (VRP) con restricción de capacidad
- **Nivel:** Avanzado
- **Tags:** vrp, routing, optimization, pulp, capacity, last-mile
- **Datasets:** Genera datos sintéticos internos
- **Tiempo estimado:** 65 min

## 60_realtime_iot/

### RT-01: Simulación de stream de tracking GPS
- **Nivel:** Intro
- **Tags:** stream, tracking, iot, async, geofencing
- **Datasets:** Genera datos sintéticos internos

## 70_ai_gen_agents/

### GEN-01: RAG (Retrieval Augmented Generation) para consultas de KPIs
- **Nivel:** Avanzado
- **Tags:** rag, llm, ai, agents, tfidf, embeddings
- **Datasets:** Corpus de KPIs internos
- **Tiempo estimado:** 60 min

## 80_governance_quality/

### DG-01: Perfilado de calidad de datos maestro
- **Nivel:** Intermedio
- **Tags:** quality, profiling, data-governance, validation
- **Datasets:** products.csv

## 90_capstone_end2end/

### CAP-01: Torre de control (dashboard integrado)
- **Nivel:** Intermedio
- **Tags:** capstone, dashboard, kpi, integration
- **Datasets:** orders.csv, inventory.csv, transport_events.csv

## 99_utilidades/

### AP-01: Apply en DataFrames - Tutorial de pandas
- **Nivel:** Intro
- **Tags:** pandas, tutorial, performance
- **Datasets:** Genera ejemplos sintéticos

### SI-09: Flujo ML end-to-end con scikit-learn
- **Nivel:** Intermedio
- **Tags:** ml, pipeline, logistic-regression, validation
- **Datasets:** orders.csv

---

**Referencia:** `config/notebooks_index.yml`
