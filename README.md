# Supply Chain Data Notebooks

**100+ Practical Notebooks for Data-Driven Supply Chain & Operations**

Repositorio de notebooks ejecutables que demuestran aplicaciones prácticas de análisis de datos, machine learning, optimización y arquitectura de datos en problemas reales de logística y operaciones.

## 📊 Estado Actual
- ✅ **6 notebooks completos** con casos de negocio realistas
- ✅ **Datos sintéticos** generados (200 SKUs, 30 ubicaciones, 8500+ órdenes)
- ✅ **5 especialidades cubiertas:** Data Engineering, Data Architecture, Data Science, Business Analytics, Optimization & OR

### Notebooks Disponibles

| ID | Título | Especialidad | Nivel | Tiempo |
|----|--------|--------------|-------|--------|
| **DE-01** | Ingesta batch desde WMS a DWH | Data Engineering | Intermedio | 45 min |
| **DA-01** | Modelo dimensional para inventarios | Data Architecture | Intermedio | 60 min |
| **DS-01** | EDA de órdenes e inventarios | Data Science | Intro | 40 min |
| **BA-01** | Dashboard OTIF (On-Time In-Full) | Business Analytics | Intermedio | 50 min |
| **OR-01** | Cálculo de stock de seguridad | Optimization & OR | Intermedio | 55 min |
| **OR-02** | VRP con restricción de capacidad | Optimization & OR | Avanzado | 65 min |

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

Ver `bases/contenido.md` para el diseño completo (100+ notebooks proyectados).

## 🚀 Próximos Pasos
- [ ] Notebooks de Real-time & IoT
- [ ] Notebooks de AI Generativa  
- [ ] Notebooks de Data Governance
- [ ] Capstones end-to-end

## 📚 Recursos
- **Especificación completa:** `bases/contenido.md`
- **Catálogo de notebooks:** `config/notebooks_index.yml`
- **Diccionario de datos:** `docs/data_dictionary.md`

## 🤝 Contribuir
Ver `CONTRIBUTING.md` para guías de estilo y proceso de contribución.

## 📝 Licencia
Este proyecto es de uso educativo y demostrativo.
