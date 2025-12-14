#!/usr/bin/env python
"""
Script para INSERTAR contextos de negocio en notebooks que no tienen sección.
Busca la mejor posición (después del título, antes de Objetivos).
"""

import json
from pathlib import Path
from typing import Tuple

# Contextos únicos por notebook ID (importar del otro script)
BUSINESS_CONTEXTS = {
    "DA-01": """## Contexto de Negocio

Analistas ejecutan queries lentas contra tablas normalizadas del operacional. Se necesita esquema diseñado específicamente para analítica rápida y autodocumentado.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Diseño dimensional (star schema) con tabla de hechos de inventario y dimensiones (producto, ubicación, tiempo, causa).
- **Por qué**: Denormalización intencional acelera queries de agregación (~100x vs OLTP), facilita joins y filtrados para BI, es estándar en industria.
- **Para qué**: Reportes de cobertura, rotación, obsolescencia; análisis de causas de variación; modelos de predicción.
- **Cuándo**: Diseño una vez, mantener dimesiones actualizadas daily (SCD Tipo 2 para historial).
- **Cómo**: Fact table con grain (producto × ubicación × día), dimensiones con surrogate keys, junk dimensions para atributos low cardinality.""",

    "DS-02": """## Contexto de Negocio

Demanda fluctúa mensualmente (picos en diciembre) pero analistas usan promedios simples. Faltan patrones estacionales en forecasts, generando stock-outs y excesos.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis de series temporales: descomposición (trend + seasonality + residual), autocorrelación, identificación de drivers estacionales.
- **Por qué**: Captar ciclos perdidos en promedios simples; mejorar forecast accuracy ~15–30%; optimizar stock según estación.
- **Para qué**: Inputs para demand planning, S&OP meetings, decisiones de compra y producción.
- **Cuándo**: Análisis anual post-Black Friday y pre-planeación Q1; re-análisis si producto nuevo o canal modificado.
- **Cómo**: Seasonal decomposition (STL), ACF/PACF plots, Box-Jenkins methodology, test de estacionaridad.""",

    "DS-04": """## Contexto de Negocio

Última milla consume 40% de costo logístico pero se planifica manualmente. Analistas desconocen drivers de costo por zona geográfica.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Análisis detallado de costo último kilómetro: desglose por zona, densidad, ruta, split entre transporte propio vs terceros.
- **Por qué**: Identificar zonas no rentables, oportunidades de consolidación, validar outsourcing vs en-house.
- **Para qué**: Decisiones de cobertura geográfica, pricing dinámico por zona, inversión en centros de distribución avanzados.
- **Cuándo**: Análisis anual; ad-hoc ante expansión a nuevas regiones.
- **Cómo**: ABC análisis por zona, regresión de costo vs variables operacionales, benchmarking vs industry.""",

    "DS-06": """## Contexto de Negocio

Demanda histórica muestra patrones predecibles (trend + seasonality). Necesidad de forecast automático para planificación integrada.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Modelado de forecast ARIMA/SARIMA: estimar demanda futura con intervalos de confianza.
- **Por qué**: Automatizar planning, reducir bias humano, cuantificar incertidumbre (95% CI) para decisiones robustas.
- **Para qué**: Input a S&OP, cálculo de stock de seguridad, presupuestos de venta, planificación de producción.
- **Cuándo**: Ejecución semanal/mensual; re-entrenar trimestralmente con nuevos datos.
- **Cómo**: Pruebas ADF/KPSS, grid search de parámetros (p,d,q), validación walk-forward, RMSE/MAPE como métricas.""",

    "BA-01": """## Contexto de Negocio

Líderes desconocen KPIs operacionales reales: ¿Cuánto % de órdenes se entregan en tiempo y completas? Respuestas varían por fuente.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Dashboard de OTIF (On Time In Full): % órdenes entregadas según SLA sin faltas.
- **Por qué**: Métrica unificada de servicio; visibilidad de causas de incumplimiento (delays, shortage); base para SLA con clientes.
- **Para qué**: Operacionales (mejorar delivery), financieras (justificar rebates), negociación con clientes.
- **Cuándo**: Dashboard live actualizado hourly; reportes diarios a gerencia.
- **Cómo**: Integración de eventos transport + órdenes, lógica de matching, dashboard Plotly/Streamlit con filtros (región, canal, cliente).""",

    "BA-02": """## Contexto de Negocio

Varias unidades son improfitables pero no se sabe por qué. Líderes necesitan desglose de costo por cliente/canal para tomar decisiones de pricing y coverage.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Cost-to-serve: desglose total de costo (COGS + logística + overhead) atribuido por cliente y canal de venta.
- **Por qué**: Visualizar clientes "vampiros" (alto servicio, bajo revenue); validar pricing; decisiones de canal.
- **Para qué**: Recomendación de pricing dinámico, decisiones de cobertura geográfica, negocios a cerrar.
- **Cuándo**: Análisis trimestral con actuals; proyecciones para S&OP.
- **Cómo**: ABC costing model, driver-based allocation (weight, distance, frequency), Pareto chart de profitabilidad.""",

    "BA-05": """## Contexto de Negocio

Ejecutivos necesitan visión integrada de operaciones sin "bajar a los detalles". Decenas de KPIs dispersos en múltiples reports.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Dashboard ejecutivo integrado: KPIs clave (OTIF, cost-to-serve, inventory, forecast accuracy, supplier risk) con narrativa clara.
- **Por qué**: Decisión rápida sin navegación de múltiples fuentes; drilldown si necesario; alineación del equipo en prioridades.
- **Para qué**: S&OP meetings, board reporting, evaluación de estrategia, identificación de acciones correctivas.
- **Cuándo**: Actualización daily; refresh en vivo durante S&OP.
- **Cómo**: Diseño de dashboard (layout, colores), KPI cards con sparklines, filtros interactivos, storytelling de anomalías.""",

    "OR-01": """## Contexto de Negocio

Stock-outs pierden ventas; exceso de stock consume capital. Necesidad de fórmula objetiva para definir cuánto stock de seguridad es "suficiente".

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Cálculo de stock de seguridad con Z-score: factor de servicio × desv. std. de demanda durante lead time.
- **Por qué**: Cuantificar el trade-off: Z=1.645 → 95% fill rate, Z=2.33 → 99%; evitar intuición subjetiva.
- **Para qué**: Definir puntos de reorden, presupuesto de capital de trabajo, evaluación de nivel de servicio alcanzable.
- **Cuándo**: Cálculo anual con revisión post-cambio de lead time o volatilidad de demanda.
- **Cómo**: Análisis estadístico de demanda e lead times, sensibilidad a Z, aplicación por categoría de SKU.""",

    "OR-02-VRP": """## Contexto de Negocio

Rutas de entrega diaria planificadas manualmente: ineficientes, costos altos, incumplimiento de SLA. Oportunidad de optimización combinatoria.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Vehicle Routing Problem (VRP): asignación óptima de clientes a vehículos minimizando distancia/tiempo/costo.
- **Por qué**: Ruteo manual es subóptimo (~30% ganancia posible); congestion, tiempo de espera son variables; solvers modernos lo resuelven en minutos.
- **Para qué**: Eficiencia de costos logísticos, cumplimiento de time windows, evaluación de flota requerida.
- **Cuándo**: Ejecución daily o según demanda; parámetros anuales (capacidad vehículo, ventanas de tiempo).
- **Cómo**: Formulación lineal con constraints, solver (OR-Tools), heurísticas (nearest neighbor, 2-opt).""",

    "GEN-01": """## Contexto de Negocio

Ejecutivos formulan preguntas de KPIs en natural language a analistas. Respuesta tarda horas. Necesidad de Q&A automatizado sobre catálogo de métricas.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Retrieval-Augmented Generation (RAG): LLM + retriever (vector DB) permite Q&A en lenguaje natural sobre documentos KPIs y políticas.
- **Por qué**: Reducir latencia (segundos vs horas), respuestas citadas (transparency), escalable a 1000+ documentos.
- **Para qué**: Self-service analytics para ejecutivos, "chatbot CFO", documentación viva.
- **Cuándo**: Query on-demand; update de índice cuando cambian políticas.
- **Cómo**: Embedding (OpenAI/open-source), vector DB (Pinecone/Chroma), LLM (GPT/Llama), evaluation de relevancia.""",

    "DG-01": """## Contexto de Negocio

Tabla maestra de productos tiene inconsistencias: duplicados, campos null, valores inválidos. Impacta todas las analíticas downstream.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Perfilado de calidad de datos: análisis profundo de completitud, validez, unicidad, consistencia de tabla maestra.
- **Por qué**: Identificar issues antes de impactar análisis; establecer baseline de calidad; SLA de data quality.
- **Para qué**: Data stewardship plan, priorización de limpiezas, evaluación de origen de datos.
- **Cuándo**: Perfilado inicial; reperfilado monthly.
- **Cómo**: Estadísticas de cobertura, patrones de nulos, validación de dominios, outlier detection.""",

    "CAP-01": """## Contexto de Negocio

Ejecutivos necesitan "comando y control" unificado: visión end-to-end de supply chain desde demand hasta delivery, con capacidad de drilldown.

## Qué / Por qué / Para qué / Cuándo / Cómo
- **Qué**: Torre de Control: integración de todas las especialidades (demand, inventory, logistics, risk, cost) en dashboard ejecutivo con narrativa clara.
- **Por qué**: Visibilidad integrada, decisión informada en vivo, alineación del equipo.
- **Para qué**: S&OP meetings, board reporting, incident management, resource allocation.
- **Cuándo**: Actualización real-time; manual drilldown según necesidad.
- **Cómo**: Diseño de UX (layout, jerarquía, interactividad), integración de datos, storytelling de anomalías, mobile-friendly.""",
}

def find_insertion_point(notebook_path: Path) -> int:
    """
    Busca el índice de celda donde insertar contexto.
    Idealmente después del título, antes de Objetivos de Aprendizaje.
    Retorna índice o -1 si no encuentra lugar apropiado.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        for i, cell in enumerate(content.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                source_text = ''.join(source) if isinstance(source, list) else source
                
                # Si encontramos "Objetivos de Aprendizaje", insertamos antes
                if 'Objetivos de Aprendizaje' in source_text:
                    return i  # Insertaremos antes de esta celda
        
        # Si no encontramos Objetivos, insertamos después de la primera celda markdown (título)
        for i, cell in enumerate(content.get('cells', [])):
            if cell.get('cell_type') == 'markdown':
                return i + 1
        
        return -1
    except:
        return -1

def insert_context(notebook_path: Path, notebook_id: str) -> bool:
    """Insertar sección de contexto en notebook."""
    try:
        context_text = BUSINESS_CONTEXTS.get(notebook_id)
        if not context_text:
            return False
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        insertion_point = find_insertion_point(notebook_path)
        if insertion_point == -1:
            print(f"  ⚠️  {notebook_id}: No se encontró punto de inserción")
            return False
        
        # Crear nueva celda markdown con contexto
        new_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + '\n' for line in context_text.split('\n')[:-1]] + [context_text.split('\n')[-1]]
        }
        
        # Insertar en el índice apropiado
        content['cells'].insert(insertion_point, new_cell)
        
        # Guardar
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=1)
        
        print(f"  ✅ {notebook_id}: Contexto insertado en posición {insertion_point}")
        return True
    
    except Exception as e:
        print(f"  ❌ {notebook_id}: Error - {e}")
        return False

def main():
    notebooks_root = Path(__file__).parent.parent / "notebooks"
    
    # Notebooks pendientes
    pending = [
        "20_data_architecture/DA-01-modelo_dimensional.ipynb",
        "30_data_science_ml/DS-02-estacionalidad.ipynb",
        "30_data_science_ml/DS-04-last_mile_analytics.ipynb",
        "30_data_science_ml/DS-06-forecast_arima.ipynb",
        "40_business_analytics_bi/BA-01-dashboard_otif.ipynb",
        "40_business_analytics_bi/BA-02-cost_to_serve.ipynb",
        "40_business_analytics_bi/BA-05-dashboard_ejecutivo.ipynb",
        "50_optimization_or/OR-01-stock_seguridad.ipynb",
        "50_optimization_or/OR-02-vrp_capacidad.ipynb",
        "70_ai_gen_agents/GEN-01-rag_kpi.ipynb",
        "80_governance_quality/DG-01-perfilado_calidad.ipynb",
        "90_capstone_end2end/CAP-01-torre_control.ipynb",
    ]
    
    print(f"\n📝 Insertando contextos en {len(pending)} notebooks...\n")
    
    updated = 0
    for rel_path in pending:
        notebook_path = notebooks_root / rel_path
        notebook_id = notebook_path.stem.split('-')[0:2]
        notebook_id = f"{notebook_id[0]}-{notebook_id[1]}"
        
        # Caso especial para OR-02-VRP
        if "vrp" in notebook_path.name.lower():
            notebook_id = "OR-02-VRP"
        
        if insert_context(notebook_path, notebook_id):
            updated += 1
    
    print(f"\n✅ {updated}/{len(pending)} notebooks actualizados\n")

if __name__ == "__main__":
    main()
