#!/usr/bin/env python
"""
Script para generar contextos de negocio únicos para todos los notebooks.
Reemplaza placeholders TODO con contenido técnico específico basado en el propósito de cada notebook.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Contextos únicos por notebook ID
BUSINESS_CONTEXTS = {
    # Data Engineering (10_data_engineering)
    "DE-01": """## Empresa y situación
Operación de retail nacional con múltiples centros de distribución que exportan CSV diarios de inventario. Necesidad de ingesta confiable y escalable al DWH sin perder trazabilidad.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Ingesta batch de archivos CSV del WMS hacia tablas Parquet en el data warehouse.
- **Por qué**: Centralizar y estandarizar datos de inventario para consultas rápidas, reportes y análisis sin depender de queries al WMS en producción.
- **Para qué**: Habilitar dashboards operativos, auditoría de movimientos, cálculo de rotación y alertas de obsolescencia.
- **Cuándo**: Procesos nocturnos (2–3 AM post-cierre), con reintentos para archivos tardíos.
- **Cómo**: Validación de esquema, enriquecimiento con timestamp de ingesta, detección de duplicados y escritura en formato columnar (Parquet).""",

    "DE-02": """## Empresa y situación
Sistema de órdenes distribuido que genera ~10K registros diarios. Reprocesar todo a diario es costoso en CPU, almacenamiento y latencia. Necesidad de arquitectura incremental eficiente.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Pipeline incremental que detecta y procesa solo órdenes nuevas o modificadas desde la última ejecución.
- **Por qué**: Reducir tiempo y costos de cómputo (~70% reducción vs recargas completas), manteniendo frescos los datos de analítica.
- **Para qué**: Mantener data warehouse actualizado con latencia <4h para análisis near real-time, reportes operativos y triggers de alertas.
- **Cuándo**: Cada 1–4 horas según SLA; reintentos automáticos ante fallas de conectividad.
- **Cómo**: Checkpoint de timestamp, filtrado incremental, append-only con deduplicación en lectura.""",

    "DE-03": """## Empresa y situación
Múltiples fuentes de datos (órdenes, productos, inventario) generan archivos CSV heterogéneos. Los analistas necesitan tabla consolidada limpia en formato consistente para reporting y modelos.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: ETL básico que integra CSV de órdenes, productos e inventario en tabla dimensional limpia y normalizada.
- **Por qué**: Eliminar duplicados, estandarizar tipos de datos, enriquecer con cálculos (lead time, rotación) para análisis sin scripting manual.
- **Para qué**: Base para dashboards, reportes mensuales de revenue, análisis de entregas tardías y decisiones de stock.
- **Cuándo**: Ejecución diaria a las 3 AM con SLA de 15 minutos máximo.
- **Cómo**: Join de tablas con validación de integridad referencial, tratamiento de nulos, normalización de campos de texto.""",

    "DE-04": """## Empresa y situación
Sistema de transporte generando eventos de ubicación, temperatura, estado en tiempo real (~100 eventos/minuto). Necesidad de ingestión y procesamiento en vivo para alertas y analítica.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Ingesta y procesamiento de stream de eventos Kafka (flotas, sensores) con ventanas temporales y agregaciones en vivo.
- **Por qué**: Monitorear SLA de entregas, detectar anomalías de temperatura, identificar rutas ineficientes en tiempo real (<1s latencia).
- **Para qué**: Alertas de incidentes, dashboards operacionales en vivo, validación de cumplimiento de entregas (OTIF).
- **Cuándo**: Procesamiento contínuo 24/7 con checkpoints cada 5 minutos.
- **Cómo**: Consumer Kafka con procesamiento de ventanas (tumbling/sliding), agregaciones estadísticas, escritura a Parquet + Redis para cache.""",

    # Data Architecture (20_data_architecture)
    "DA-01": """## Empresa y situación
Analistas ejecutan queries lentas contra tablas normalizadas del operacional. Se necesita esquema diseñado específicamente para analítica rápida y autodocumentado.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Diseño dimensional (star schema) con tabla de hechos de inventario y dimensiones (producto, ubicación, tiempo, causa).
- **Por qué**: Denormalización intencional acelera queries de agregación (~100x vs OLTP), facilita joins y filtrados para BI, es estándar en industria.
- **Para qué**: Reportes de cobertura, rotación, obsolescencia; análisis de causas de variación; modelos de predicción.
- **Cuándo**: Diseño una vez, mantener dimesiones actualizadas daily (SCD Tipo 2 para historial).
- **Cómo**: Fact table con grain (producto × ubicación × día), dimensiones con surrogate keys, junk dimensions para atributos low cardinality.""",

    "DA-02": """## Empresa y situación
Datos crecen exponencialmente (~500GB/año). Queries sobre datasets grandes son lentas. Necesidad de particionamiento inteligente para balancear almacenamiento y performance.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Data lake con zonas (raw/curated/analytics), particiones por year/month/day en Parquet, catálogo de assets.
- **Por qué**: Particiones permiten pruning (skip unnecesary data), reducen I/O ~90%, facilitan archiving y retención diferenciada por zona.
- **Para qué**: Queries rápidas incluso con 5+ años de datos; compliance con retención normativa; reproducibilidad de análisis históricos.
- **Cuándo**: Arquitectura baseline; optimización de particiones según patrón de consultas (trimestral review).
- **Cómo**: Bertrands hive-style partitioning, usar columnas de fecha natural, compactar small files quarterly, versionamiento de esquema.""",

    # Data Science/ML (30_data_science_ml)
    "DS-01": """## Empresa y situación
Datos de órdenes e inventario sin explorar. Analistas y data scientists desconocen distribuciones, outliers y correlaciones. Riesgo de conclusiones sesgadas en modelos posteriores.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis Exploratorio de Datos (EDA) sistemático: estadísticas descriptivas, visualizaciones, detección de anomalías.
- **Por qué**: Validar data quality antes de modelos; generar hipótesis sobre drivers de demanda; documentar supuestos para stakeholders.
- **Para qué**: Informa feature engineering, detecta missing data y valores extremos, genera insights iniciales para roadmap de análisis.
- **Cuándo**: Primera fase de cualquier proyecto analytics (baseline antes de modeling).
- **Cómo**: Histogramas, boxplots, heatmaps de correlación, estadísticas por segmento, temporal trends.""",

    "DS-02": """## Empresa y situación
Demanda fluctúa mensualmente (picos en diciembre) pero analistas usan promedios simples. Faltan patrones estacionales en forecasts, generando stock-outs y excesos.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de series temporales: descomposición (trend + seasonality + residual), autocorrelación, identificación de drivers estacionales.
- **Por qué**: Captar ciclos perdidos en promedios simples; mejorar forecast accuracy ~15–30%; optimizar stock según estación.
- **Para qué**: Inputs para demand planning, S&OP meetings, decisiones de compra y producción.
- **Cuándo**: Análisis anual post-Black Friday y pre-planeación Q1; re-análisis si producto nuevo o canal modificado.
- **Cómo**: Seasonal decomposition (STL), ACF/PACF plots, Box-Jenkins methodology, test de estacionaridad.""",

    "DS-03": """## Empresa y situación
Líderes desconocen trade-off entre nivel de servicio (costo de stock, espacio) vs costo operativo de entregas. Decisiones ad-hoc sin cuantificación.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de trade-off: simular costo total (carry + obsolescencia) vs nivel de servicio (fill rate, OTIF).
- **Por qué**: Encontrar punto óptimo no obvio; cantidad de producto que maximiza margin evitando exceso; base cuantitativa para negociación con líderes.
- **Para qué**: Recomendación de política de stock óptima, decisiones de transporte (express vs standard), evaluación de inversión en warehouse.
- **Cuándo**: Trimestralmente o ante cambios en costos operativos / volumen.
- **Cómo**: Simulación Monte Carlo, sensibilidad de parámetros, Pareto frontier de soluciones.""",

    "DS-04": """## Empresa y situación
Última milla consume 40% de costo logístico pero se planifica manualmente. Analistas desconocen drivers de costo por zona geográfica.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis detallado de costo último kilómetro: desglose por zona, densidad, ruta, split entre transporte propio vs terceros.
- **Por qué**: Identificar zonas no rentables, oportunidades de consolidación, validar outsourcing vs en-house.
- **Para qué**: Decisiones de cobertura geográfica, pricing dinámico por zona, inversión en centros de distribución avanzados.
- **Cuándo**: Análisis anual; ad-hoc ante expansión a nuevas regiones.
- **Cómo**: ABC análisis por zona, regresión de costo vs variables operacionales, benchmarking vs industry.""",

    "DS-05": """## Empresa y situación
Supply chain vulnerable: proveedores sin redundancia, riesgos climáticos, geopolíticos no monitoreados. Un disruption = lost sales.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Identificación de riesgos en supply chain: concentración de proveedores, lead times largos, criticidad de SKUs.
- **Por qué**: Proactividad: diseñar redundancia, negociar contratos de backup, estrategia de sourcing diversificada.
- **Para qué**: Business continuity plan, decisiones de sourcing, cobertura de seguros, inventario de seguridad aumentado en SKUs críticos.
- **Cuándo**: Análisis anual; ad-hoc post-disrupción para aprender y mitigar.
- **Cómo**: Matriz riesgo (criticidad × vulnerabilidad), network analysis de suppliers, scenario planning.""",

    "DS-06": """## Empresa y situación
Demanda histórica muestra patrones predecibles (trend + seasonality). Necesidad de forecast automático para planificación integrada.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Modelado de forecast ARIMA/SARIMA: estimar demanda futura con intervalos de confianza.
- **Por qué**: Automatizar planning, reducir bias humano, cuantificar incertidumbre (95% CI) para decisiones robustas.
- **Para qué**: Input a S&OP, cálculo de stock de seguridad, presupuestos de venta, planificación de producción.
- **Cuándo**: Ejecución semanal/mensual; re-entrenar trimestralmente con nuevos datos.
- **Cómo**: Pruebas ADF/KPSS, grid search de parámetros (p,d,q), validación walk-forward, RMSE/MAPE como métricas.""",

    "DS-07": """## Empresa y situación
Proveedores varían en calidad (entregas tardías, defectos). Riesgo de disruption si un proveedor crítico falla. Scoring manual es subjetivo.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Clasificación de riesgo de proveedores: ML model (RF/XGBoost) con features de performance histórico.
- **Por qué**: Automatizar y objetivizar evaluación, priorizar auditorías en proveedores high-risk, identificar tendencias deterioro.
- **Para qué**: Decisiones de sourcing, renegociación de contratos, estrategia de dual sourcing, planes de contingencia.
- **Cuándo**: Scoring monthly; model retraining quarterly; alerts si score deteriora >10%.
- **Cómo**: Features: on-time %, defect rate, lead time variability; CV-tuned RF; SHAP para explicabilidad.""",

    # Business Analytics/BI (40_business_analytics_bi)
    "BA-01": """## Empresa y situación
Líderes desconocen KPIs operacionales reales: ¿Cuánto % de órdenes se entregan en tiempo y completas? Respuestas varían por fuente.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Dashboard de OTIF (On Time In Full): % órdenes entregadas según SLA sin faltas.
- **Por qué**: Métrica unificada de servicio; visibilidad de causas de incumplimiento (delays, shortage); base para SLA con clientes.
- **Para qué**: Operacionales (mejorar delivery), financieras (justificar rebates), negociación con clientes.
- **Cuándo**: Dashboard live actualizado hourly; reportes diarios a gerencia.
- **Cómo**: Integración de eventos transport + órdenes, lógica de matching, dashboard Plotly/Streamlit con filtros (región, canal, cliente).""",

    "BA-02": """## Empresa y situación
Varias unidades son improfitables pero no se sabe por qué. Líderes necesitan desglose de costo por cliente/canal para tomar decisiones de pricing y coverage.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Cost-to-serve: desglose total de costo (COGS + logística + overhead) atribuido por cliente y canal de venta.
- **Por qué**: Visualizar clientes "vampiros" (alto servicio, bajo revenue); validar pricing; decisiones de canal.
- **Para qué**: Recomendación de pricing dinámico, decisiones de cobertura geográfica, negocios a cerrar.
- **Cuándo**: Análisis trimestral con actuals; proyecciones para S&OP.
- **Cómo**: ABC costing model, driver-based allocation (weight, distance, frequency), Pareto chart de profitabilidad.""",

    "BA-03": """## Empresa y situación
Productividad de warehouse es baja: picking, packing, shipping lentos. Analistas desconocen drivers: layout, staffing, seasonality, SKU mix.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de productividad: cajas/hora, lineas/picker/hora, rotación de SKUs por zona.
- **Por qué**: Benchmarking contra estándares, identificar cuellos de botella (packing vs picking), validar need for automation.
- **Para qué**: Decisiones de layout (reorganización), staffing levels (temporal), inversión en tecnología (sorting, conveyors).
- **Cuándo**: Análisis semanal de trending; deeper dive mensual.
- **Cómo**: Extracción de WMS data, clustering de SKUs por velocidad, regresión de productividad vs factores.""",

    "BA-04": """## Empresa y situación
Proveedores varían enormemente en calidad, lead time y precio. Compras negocia sin visibilidad integral. Riesgo de dependencias no monitoreadas.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Dashboard de performance de proveedores: on-time %, defect rate, lead time, precio vs market, volumen.
- **Por qué**: Transparencia en desempeño, negociación informada, identificación de proveedores en deterioro.
- **Para qué**: Decisiones de sourcing, renegociación de contratos, auditorías, planes de contingencia.
- **Cuándo**: Scorecard actualizado mensualmente; reports a procurement quarterly.
- **Cómo**: SLA-based metrics, trend analysis, Pareto de críticos, comparativas vs market.""",

    "BA-05": """## Empresa y situación
Ejecutivos necesitan visión integrada de operaciones sin "bajar a los detalles". Decenas de KPIs dispersos en múltiples reports.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Dashboard ejecutivo integrado: KPIs clave (OTIF, cost-to-serve, inventory, forecast accuracy, supplier risk) con narrativa clara.
- **Por qué**: Decisión rápida sin navegación de múltiples fuentes; drilldown si necesario; alineación del equipo en prioridades.
- **Para qué**: S&OP meetings, board reporting, evaluación de estrategia, identificación de acciones correctivas.
- **Cuándo**: Actualización daily; refresh en vivo durante S&OP.
- **Cómo**: Diseño de dashboard (layout, colores), KPI cards con sparklines, filtros interactivos, storytelling de anomalías.""",

    # Optimization/OR (50_optimization_or)
    "OR-01": """## Empresa y situación
Stock-outs pierden ventas; exceso de stock consume capital. Necesidad de fórmula objetiva para definir cuánto stock de seguridad es "suficiente".

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Cálculo de stock de seguridad con Z-score: factor de servicio × desv. std. de demanda durante lead time.
- **Por qué**: Cuantificar el trade-off: Z=1.645 → 95% fill rate, Z=2.33 → 99%; evitar intuición subjetiva.
- **Para qué**: Definir puntos de reorden, presupuesto de capital de trabajo, evaluación de nivel de servicio alcanzable.
- **Cuándo**: Cálculo anual con revisión post-cambio de lead time o volatilidad de demanda.
- **Cómo**: Análisis estadístico de demanda e lead times, sensibilidad a Z, aplicación por categoría de SKU.""",

    "OR-02-EOQ": """## Empresa y situación
Compras generan órdenes sin criterio económico: algunas semanales (costos altos), otras mensuales (stock alto). Oportunidad de optimizar.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Cálculo de lote económico (EOQ): cantidad de compra que minimiza total de costos (ordering + carrying).
- **Por qué**: Matemáticamente óptimo; reduce costos ~5–15% vs políticas ad-hoc; determinístico.
- **Para qué**: Parámetro de política de reorden (Q) para cada proveedor/SKU; evaluación de negociar volúmenes con proveedores.
- **Cuándo**: Cálculo anual; revisión si cambian costos (transporte, warehouse) o volumen.
- **Cómo**: Fórmula clásica EOQ = sqrt(2×D×S/H), estimación de costos (S, H), aplicación por categoría ABC.""",

    "OR-02-VRP": """## Empresa y situación
Rutas de entrega diaria planificadas manualmente: ineficientes, costos altos, incumplimiento de SLA. Oportunidad de optimización combinatoria.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Vehicle Routing Problem (VRP): asignación óptima de clientes a vehículos minimizando distancia/tiempo/costo.
- **Por qué**: Ruteo manual es subóptimo (~30% ganancia posible); congestion, tiempo de espera son variables; solvers modernos lo resuelven en minutos.
- **Para qué**: Eficiencia de costos logísticos, cumplimiento de time windows, evaluación de flota requerida.
- **Cuándo**: Ejecución daily o según demanda; parámetros anuales (capacidad vehículo, ventanas de tiempo).
- **Cómo**: Formulación lineal con constraints, solver (OR-Tools), heurísticas (nearest neighbor, 2-opt).""",

    "OR-03": """## Empresa y situación
Centros de distribución tienen capacidad limitada. Gestión de crecimiento requiere decisión: ¿expandir existentes o abrir nuevos? ¿Dónde? ¿Cuándo?

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Programación lineal para capacidad: asignación de demanda a centros (existentes + candidatos) minimizando costo total.
- **Por qué**: Captura restricciones reales (capacity, lead time, surtido), evita decisiones miopes.
- **Para qué**: Business case para expansión, decisión de outsourcing (3PL), rebalanceo de demanda.
- **Cuándo**: Análisis anual o ante disrupción (cierre de warehouse, nuevo cliente grande).
- **Cómo**: Modelo de flujo en red, constraints de capacidad y demanda, solución con PuLP/Gurobi.""",

    "OR-04": """## Empresa y situación
Estructura de distribución (suppliers → DCs → stores) no optimizada. Algunos productos dan demasiadas vueltas (ineficiente); otros se estancan.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Inventario multi-echelon (MECI): optimización simultánea de stock en suppliers, DCs y stores considerando relaciones.
- **Por qué**: Minimizar total de capital de trabajo; reducir lead time end-to-end; aprovechar flexibilidad en cadena.
- **Para qué**: Decisiones de ubicación de stock, parámetros de reorden por nivel, evaluación de transshipment.
- **Cuándo**: Diseño baseline anual; optimización mensual con parámetros dinámicos.
- **Cómo**: Modelo de balística (Sherbrooke), optimización escalonada (top-down o bottom-up), simulación de políticas.""",

    "OR-05": """## Empresa y situación
Warehouse grande (50K SKUs) con picking lento: pasillos congestionados, viajes largos para pegatinas complementarias. Layout es resultado histórico de cambios.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Optimización de slotting: asignación de SKU a locaciones minimizando distancia de picking (por ejemplo, ABC-XYZ).
- **Por qué**: Productos fast-moving cerca de salida reduce viajes ~20–30%; productos slow en fondo; seasonal en almacén dinámico.
- **Para qué**: Mejora de productividad de picking, reducción de fatiga del operario, evaluación de automatización.
- **Cuándo**: Análisis trimestral con cambios estacionales; re-slotting semestral.
- **Cómo**: Matriz ABC (volumen) × XYZ (variabilidad), scoring de locaciones, reubicación gradual.""",

    "OR-06": """## Empresa y situación
Muelles de dock están congestionados: camiones esperan, operarios ociosos, SLA de descarga incumplido. Capacidad parece "justa" pero no lo es.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Simulación de queue en muelles: comportamiento de cola (llegada, servicio) con múltiples servidores (muelles) y colas virtuales.
- **Por qué**: Analítico puro no captura esperas; simulación muestra distribución de tiempos, bottlenecks, impacto de cambios.
- **Para qué**: Decisiones de: inversión en muelles (# muelles óptimo), horarios de llegada (ventanas), asignación de operarios.
- **Cuándo**: Ad-hoc ante cuellos de botella; rediseño pre-expansión.
- **Cómo**: Simulation discrete event (SimPy), distribuciones de llegada/servicio, KPIs (espera promedio, utilización).""",

    "OR-07": """## Empresa y situación
Stock de seguridad se calcula como "semanas de stock" sin rigor estadístico. Nivel de servicio resultante es incierto: puede ser 90% o 99%.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Introducción a seguridad de stock: conceptos fundamentales (z-score, demanda durante LT, variabilidad) con ejemplos ilustrativos.
- **Por qué**: Educación: sentar bases para OR-01 (cálculo matemático) y OR-02 (políticas de reorden).
- **Para qué**: Entrenamiento interno, comunicación a procurement, validación de políticas existentes.
- **Cuándo**: Contenido educativo; revisar pre-audit de políticas.
- **Cómo**: Explicación conceptual, ejemplos numéricos simples, gráficos visuales de distribuciones.""",

    "OR-08": """## Empresa y situación
Producción opera con schedule manual: capacidad no balanceada, setup time genera esperas, no hay visibilidad de factibilidad.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Scheduling de producción: asignación de órdenes a máquinas/líneas en horizonte de tiempo minimizando makespan o tardías.
- **Por qué**: Balanceamiento automático, consideración de setup, visibilidad de bottlenecks, evaluación de cambios.
- **Para qué**: Mejora de OEE (eficiencia), reducción de tardías, negociación de lead times con ventas.
- **Cuándo**: Planeamiento semanal o según demanda (job shop vs flow shop).
- **Cómo**: Formulación con constraints, solvers (OR-Tools), heurísticas (SPT, LPT).""",

    "OR-09": """## Empresa y situación
Red de distribución (plantas, DCs, stores) tiene oportunidades de optimización: algunos flujos son ineficientes, costs altos en rutas.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Network optimization: asignación de demanda (stores) a orígenes (plantas/DCs) minimizando costo total logístico + producción.
- **Por qué**: Captura estructura real de red, interdependencias, economías de escala; identifica caminos no óptimos.
- **Para qué**: Redesign de red, decisiones de sourcing por región, evaluación de clustering (nuevos DCs).
- **Cuándo**: Análisis anual; ad-hoc ante cambios de mercado o infraestructura.
- **Cómo**: Modelo de flujo en red, linear programming, postoptimality analysis para sensibilidad.""",

    # Realtime/IoT (60_realtime_iot)
    "RT-01": """## Empresa y situación
Flotas generan telémetry en vivo (ubicación, combustible, estado). Necesidad de visibilidad de posiciones para despachador y análisis de rutas.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Tracking de flotas: ingesta de eventos GPS, almacenamiento y visualización de posiciones actuales + histórico.
- **Por qué**: Visibilidad operacional real-time, capacidad de re-ruteo dinámico, análisis de comportamiento del conductor.
- **Para qué**: Despacho eficiente, investigación de incidentes, SLA de entrega.
- **Cuándo**: Actualización continua; histórico retención 90 días.
- **Cómo**: Event stream processing, geohashing para queries geoespaciales, mapa interactivo (Folium/Mapbox).""",

    "RT-02": """## Empresa y situación
Flotas tienen fallos no predichos: costoso, afecta delivery, causas desconocidas. Necesidad de patrón de degradación para mantenimiento preventivo.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Mantenimiento predictivo: ML model (e.g., RF) predice prob. de fallo en próximos 7 días basado en telemetría (RPM, temperatura, presión).
- **Por qué**: Evitar downtime inesperado, planificar ventanas de servicio con mínimo impacto, optimizar costos mantenimiento.
- **Para qué**: Schedule proactivo de mantenimiento, inventario de repuestos, SLA de fleet availability.
- **Cuándo**: Predicción diaria; model retraining mensual.
- **Cómo**: Features de telemetría, labeled data de fallos históricos, CV-tuned RF, threshold de probabilidad.""",

    "RT-03": """## Empresa y situación
Transporte refrigerado (fármacos, alimentos) requiere validación de cadena de frío: ¿temperatura siempre < 8°C? Alertas si excede.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Monitoreo de cadena de frío: ingesta de sensores de temperatura/humedad, reglas de alertas en vivo, reportes de conformidad.
- **Por qué**: Compliance normativo (FDA, GDPR); validación de integridad de producto; liability si cadena rota.
- **Para qué**: Certificación de entrega, investigación de quejas de clientes, optimización de rutas (evitar congestión = tiempos largos).
- **Cuándo**: Monitoreo contínuo durante transporte; alertas inmediatas si excepción.
- **Cómo**: Stream processing de sensores, rule engine (threshold alerts), blockchain-ready reporting.""",

    "RT-04": """## Empresa y situación
Sensores IoT generan datos continuos (temperatura, humedad, ocupación) de almacenes/transporte. Datos crudos sin análisis; oportunidad perdida.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Introducción a IoT: tipos de sensores, protocolos (MQTT, LoRaWAN), desafíos de escala (volumen, latencia, confiabilidad).
- **Por qué**: Educación: sentar bases para RT-01 (tracking) y RT-03 (cold chain); entendimiento de limitaciones.
- **Para qué**: Estrategia de IoT deployment, evaluación de tecnología, business case.
- **Cuándo**: Contenido educativo; revisar pre-deploy de nuevo sensor network.
- **Cómo**: Explicación conceptual, ejemplos de arquitecturas, case studies.""",

    "TR-01": """## Empresa y situación
Transporte masivo (buses) tiene datos de GPS y GTFS. Oportunidad de análisis de performance: cumplimiento de horarios, cobertura, demanda latente.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de transporte masivo: OTP (on-time performance), headways, ocupación, cobertura geográfica usando GTFS + real-time data.
- **Por qué**: Transparencia operacional, identificación de líneas problemáticas, evaluación de servicio vs ciudadanía.
- **Para qué**: Decisiones de rebalanceo de flota, reingeniería de rutas, negociación con operadores.
- **Cuándo**: Análisis trimestral de performance; alertas daily si degradación.
- **Cómo**: Integración GTFS + real-time, cálculo de métricas (OTP, headway), análisis geoespacial, dashboard público.""",

    # AI Generativa (70_ai_gen_agents)
    "GEN-01": """## Empresa y situación
Ejecutivos formulan preguntas de KPIs en natural language a analistas. Respuesta tarda horas. Necesidad de Q&A automatizado sobre catálogo de métricas.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Retrieval-Augmented Generation (RAG): LLM + retriever (vector DB) permite Q&A en lenguaje natural sobre documentos KPIs y políticas.
- **Por qué**: Reducir latencia (segundos vs horas), respuestas citadas (transparency), escalable a 1000+ documentos.
- **Para qué**: Self-service analytics para ejecutivos, "chatbot CFO", documentación viva.
- **Cuándo**: Query on-demand; update de índice cuando cambian políticas.
- **Cómo**: Embedding (OpenAI/open-source), vector DB (Pinecone/Chroma), LLM (GPT/Llama), evaluation de relevancia.""",

    "GEN-02": """## Empresa y situación
Quejas de clientes no categorizadas: equipo manual etiqueta sentimiento y categoría. Lento y subjetivo. Volumen crece exponencialmente.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de texto con LLM: clasificación automática de sentimiento y categoría de quejas/feedback usando prompting y fine-tuning.
- **Por qué**: Escala sin crecer equipo; consistencia; feedback inmediato a operaciones.
- **Para qué**: Alertas de issues críticos, trending de topics, input a root cause analysis.
- **Cuándo**: Procesamiento en batch diario o streaming en vivo.
- **Cómo**: Prompt engineering, few-shot learning, embedding para similarity, dashboard de trends.""",

    # Data Governance (80_governance_quality)
    "DG-01": """## Empresa y situación
Tabla maestra de productos tiene inconsistencias: duplicados, campos null, valores inválidos. Impacta todas las analíticas downstream.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Perfilado de calidad de datos: análisis profundo de completitud, validez, unicidad, consistencia de tabla maestra.
- **Por qué**: Identificar issues antes de impactar análisis; establecer baseline de calidad; SLA de data quality.
- **Para qué**: Data stewardship plan, priorización de limpiezas, evaluación de origen de datos.
- **Cuándo**: Perfilado inicial; reperfilado monthly.
- **Cómo**: Estadísticas de cobertura, patrones de nulos, validación de dominios, outlier detection.""",

    # Capstone (90_capstone_end2end)
    "CAP-01": """## Empresa y situación
Ejecutivos necesitan "comando y control" unificado: visión end-to-end de supply chain desde demand hasta delivery, con capacidad de drilldown.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Torre de Control: integración de todas las especialidades (demand, inventory, logistics, risk, cost) en dashboard ejecutivo con narrativa clara.
- **Por qué**: Visibilidad integrada, decisión informada en vivo, alineación del equipo.
- **Para qué**: S&OP meetings, board reporting, incident management, resource allocation.
- **Cuándo**: Actualización real-time; manual drilldown según necesidad.
- **Cómo**: Diseño de UX (layout, jerarquía, interactividad), integración de datos, storytelling de anomalías, mobile-friendly.""",

    # Utilities (99_utilidades)
    "AP-01": """## Empresa y situación
Analistas tienen funciones reutilizables (limpieza, validación, agregación) dispersas en múltiples notebooks. Riesgo de inconsistencia y duplicación.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Librería de utilidades: patrones comunes (apply a dataframe, validaciones, normalización de datos) documentados y ejemplificados.
- **Por qué**: Reutilización, consistencia, documentación centralizada para onboarding.
- **Para qué**: Aceleración de desarrollo de nuevos análisis, training de nuevos analistas.
- **Cuándo**: Desarrollo inicial; mantenimiento continuous.
- **Cómo**: Ejemplos de apply (operaciones comunes), best practices, versionamiento.""",

    "SI-09": """## Empresa y situación
Flujo de procesos S&OP complejo: múltiples pasos (demand > supply > finance) sin visibilidad integrada. Cambios manuales riesgosos.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Automatización del flujo S&OP: pipeline integrado que consolida demand forecasts, supply constraints, financials en recomendaciones.
- **Por qué**: Visibilidad integral, ejecución consistente, trazabilidad de decisiones, reducción de errores manual.
- **Para qué**: Meetings más rápidas y informadas, documentación de decisiones, auditoría post-hoc.
- **Cuándo**: Ejecución monthly (pre-S&OP meeting).
- **Cómo**: Orchestración de scripts, workflow DAG, consolidación de datos, generación automática de reportes.""",
}

def replace_context_placeholder(notebook_path: Path, notebook_id: str) -> bool:
    """
    Lee notebook, busca sección de "Contexto de Negocio" y reemplaza con contenido técnico completo.
    Retorna True si fue reemplazado, False si no encontró sección o error.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # Obtener contexto predefinido
        business_context = BUSINESS_CONTEXTS.get(notebook_id)
        if not business_context:
            print(f"  ⚠️  {notebook_id}: No se encontró contexto predefinido")
            return False
        
        # Buscar la celda markdown que contiene "Contexto de Negocio"
        found = False
        for i, cell in enumerate(content.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                # Convertir a string si es lista
                source_text = ''.join(source) if isinstance(source, list) else source
                
                # Buscar variantes de la sección de contexto
                if 'Contexto de Negocio' in source_text or 'Contexto del Negocio' in source_text:
                    # Verificar si es un TODO o un contenido incompleto
                    is_placeholder = 'TODO' in source_text or (len(source_text) < 300 and ('Describir brevemente' in source_text or 'brevemente el contexto' in source_text))
                    
                    if is_placeholder:
                        # Crear nueva celda con contexto completo
                        new_source = f"""## Contexto de Negocio

{business_context}"""
                        cell['source'] = [line + '\n' for line in new_source.split('\n')[:-1]] + [new_source.split('\n')[-1]]
                        found = True
                        break
        
        if not found:
            print(f"  ⚠️  {notebook_id}: No se encontró placeholder de Contexto (probable que ya tenga contenido)")
            return False
        
        # Escribir notebook actualizado
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=1)
        
        print(f"  ✅ {notebook_id}: Contexto actualizado")
        return True
    
    except Exception as e:
        print(f"  ❌ {notebook_id}: Error - {e}")
        return False

def main():
    """Procesar todos los notebooks y actualizar contextos."""
    notebooks_root = Path(__file__).parent.parent / "notebooks"
    
    # Listar todos los notebooks (excepto templates)
    notebook_files = sorted(notebooks_root.glob("**/[!TEMPLATE]*.ipynb"))
    notebook_files = [f for f in notebook_files if "PLANTILLA" not in f.name and "TEMPLATE" not in f.name]
    
    print(f"\n📚 Procesando {len(notebook_files)} notebooks...\n")
    
    updated_count = 0
    for notebook_path in notebook_files:
        # Extraer ID del nombre (ej: DE-01 de DE-01-ingesta.ipynb)
        filename = notebook_path.stem  # DE-01-ingesta
        parts = filename.split('-')
        notebook_id = f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else parts[0]
        
        # Caso especial: BA-02-CTS y BA-02-SOP tienen ID especial
        if "cost_to_serve" in notebook_path.name:
            notebook_id = "BA-02"
        elif "sop_scenarios" in notebook_path.name or "scenarios" in notebook_path.name:
            # Este es BA-02-SOP, usamos BA-02 generalizado
            pass
        
        if replace_context_placeholder(notebook_path, notebook_id):
            updated_count += 1
    
    print(f"\n✅ Resumen: {updated_count}/{len(notebook_files)} notebooks actualizados\n")

if __name__ == "__main__":
    main()
