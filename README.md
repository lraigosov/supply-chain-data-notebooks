# Supply Chain Data Notebooks

**100+ Practical Notebooks for Data-Driven Supply Chain & Operations**

Repositorio de notebooks ejecutables que demuestran aplicaciones prácticas de análisis de datos, machine learning, optimización y arquitectura de datos en problemas reales de logística y operaciones.

## 📊 Estado Actual
- ✅ **16 notebooks implementados** con casos de negocio realistas
- ✅ **Datos sintéticos** generados (200 SKUs, 30 ubicaciones, 8500+ órdenes)
- ✅ **9 especialidades cubiertas:** Data Engineering, Data Architecture, Data Science, Business Analytics, Optimization & OR, Real-time & IoT, AI Generativa, Data Governance, Capstone

### Notebooks Implementados

| ID | Título | Especialidad | Nivel | Tiempo |
|----|--------|--------------|-------|--------|
| **DE-01** | Ingesta batch desde WMS a DWH | Data Engineering | Intermedio | 45 min |
| **DE-02** | Pipeline incremental de órdenes | Data Engineering | Intermedio | - |
| **DA-01** | Modelo dimensional para inventarios | Data Architecture | Intermedio | 60 min |
| **DS-01** | EDA de órdenes e inventarios | Data Science | Intro | 40 min |
| **DS-02** | Detección de estacionalidad en demanda | Data Science | Intermedio | - |
| **BA-01** | Dashboard OTIF (On-Time In-Full) | Business Analytics | Intermedio | 50 min |
| **OR-01** | Cálculo de stock de seguridad | Optimization & OR | Intermedio | 55 min |
| **OR-02** | Políticas de inventario | Optimization & OR | Intermedio | - |
| **OR-02** | VRP con restricción de capacidad | Optimization & OR | Avanzado | 65 min |
| **RT-01** | Simulación de stream de tracking | Real-time & IoT | Intro | - |
| **GEN-01** | RAG para consultas de KPIs | AI Generativa | Avanzado | 60 min |
| **DG-01** | Perfilado de calidad de datos maestro | Data Governance | Intermedio | - |
| **CAP-01** | Torre de control (dashboard integrado) | Capstone | Intermedio | - |
| **AP-01** | Apply en DataFrames (tutorial pandas) | Utilidades | Intro | - |
| **SI-09** | Flujo ML end-to-end | Utilidades | Intermedio | - |

Cada notebook incluye:
- 📋 **Contexto de negocio real** (retail, farmacéutica, logística)
- 🎯 **Explicación Qué/Por qué/Para qué/Cuándo/Cómo**
- 📊 **Código ejecutable** con datos sintéticos realistas
- 📈 **Visualizaciones** y análisis detallados
- 💡 **Insights accionables** y recomendaciones

## Requisitos
- Python 3.11+
- PowerShell (Windows)

## Setup
```powershell
# Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -U pip
pip install pandas numpy matplotlib seaborn plotly scipy pyyaml pyarrow pulp
```

## Generar datos sintéticos
```powershell
python data/synthetic_generators/generate_data.py
```

## Ejecutar un notebook
```powershell
# Con papermill
papermill notebooks/20_data_architecture/DA-01-modelo_dimensional.ipynb output.ipynb

# O abrir directamente en Jupyter/VS Code
jupyter notebook
```

## 📁 Estructura del Proyecto
```
.
├── data/
│   ├── raw/               # Datos sintéticos (CSV)
│   ├── processed/         # Datos transformados
│   └── synthetic_generators/  # Scripts para generar datos
├── notebooks/
│   ├── 10_data_engineering/
│   ├── 20_data_architecture/
│   ├── 30_data_science_ml/
│   ├── 40_business_analytics_bi/
│   ├── 50_optimization_or/
│   └── ...
├── src/
│   └── utils/             # Módulos reutilizables
├── config/
│   └── notebooks_index.yml  # Catálogo de notebooks
└── docs/                  # Documentación adicional
```

**Nota:** La carpeta `bases/` está ignorada por Git y no forma parte del repositorio.

## 📚 Recursos
- **Catálogo de notebooks:** `config/notebooks_index.yml`
- **Diccionario de datos:** `docs/data_dictionary.md`
- **Análisis de notebooks:** `ANALISIS_NOTEBOOKS.md`

## 📝 Licencia
Este proyecto es de uso educativo y demostrativo.
