# Guía de Contribución

Gracias por tu interés en mejorar este repositorio. Esta guía te ayudará a crear notebooks de alta calidad para líderes de supply chain.

## Antes de empezar

1. **Revisa el catálogo**: `python -m scripts.catalog list` para ver qué notebooks existen
2. **Elige tu especialidad**: Data Engineering, Analytics, BI, OR, IoT, GenAI, Governance, etc.
3. **Verifica nivel**: ¿Es intro, intermedio o avanzado?

## Crear un nuevo notebook

### 1. Nombre y ubicación

- **Patrón**: `{PREFIJO}-{número}-{descripción}.ipynb`
- **Ejemplo**: `DS-06-demand_forecasting_arima.ipynb`
- **Ubicación**: `notebooks/{numero}_categoria/`

| Número | Categoría | Prefijo |
|--------|-----------|---------|
| 10 | Data Engineering | DE |
| 20 | Data Architecture | DA |
| 30 | Data Science/ML | DS |
| 40 | Business Analytics/BI | BA |
| 50 | Optimization/OR | OR |
| 60 | Realtime/IoT | RT |
| 70 | AI Generativa | GEN |
| 80 | Data Governance | DG |
| 90 | Capstone | CAP |
| 99 | Utilidades | (varies) |

### 2. Estructura mínima (plantilla)

Tu notebook **debe iniciar** con metadatos YAML en la primera celda (markdown):

```yaml
---
title: "Título Descriptivo del Notebook"
objective: |
  Qué aprenderá el líder de supply chain al ejecutar este notebook.
  Máximo 2-3 líneas, objetivo claro y medible.
level: "Intro"  # o "Intermediate", "Advanced"
duration_min: 45
datasets:
  - orders.csv
  - inventory.csv
tags:
  - eda
  - analytics
  - kpi
author: "Tu Nombre"
process: "Plan"  # Source, Make, Deliver, Plan, Enable, Return
specialty: "Data Science"
---
```

**Campos obligatorios**:
- `title`, `objective`, `level`, `duration_min`, `datasets`, `tags`

**Campos opcionales**:
- `author`, `process`, `specialty`

### 3. Secciones recomendadas

```
1. Metadatos YAML (celda 1 - markdown)
2. Objetivos y contexto (markdown)
3. Carga de librerías (python)
4. Carga y exploración de datos (python)
5. Análisis principal (python + markdown)
6. Conclusiones y siguientes pasos (markdown)
7. Código reutilizable (python, opcional)
```

### 4. Buenas prácticas

#### 📊 Datos
- Usa datos de `data/raw/`
- Documenta qué CSVs necesitas en metadatos `datasets`
- Maneja valores ausentes y outliers explícitamente

#### 📝 Código
- Añade comentarios explicativos, no obvios
- Usa nombres descriptivos: `customer_orders_monthly` vs `df`
- Limita líneas largas a ~100 caracteres
- Agrupa código lógico con comentarios tipo `# === Sección ===#`

#### 📈 Visualizaciones
- Usa `plotly` para gráficos interactivos (preferente)
- Añade títulos y etiquetas descriptivas
- Colores consistentes con el tema del repositorio

#### ⏱️ Tiempo
- `Intro`: 15-30 min (máx 100 líneas de código)
- `Intermediate`: 30-60 min (máx 300 líneas)
- `Advanced`: 60+ min (máx 600 líneas)

#### 🎯 Audiencia
- Explica conceptos para **líderes**, no solo data scientists
- Incluye contexto de supply chain
- Termina con "qué significa esto para mi operación"

### 5. Usar datos sintéticos

Genera datos de prueba localmente:

```bash
# Modo rápido (7 días, 20 SKUs) - ideal para desarrollo
python data/synthetic_generators/generate_cli.py --fast

# Modo completo (90 días, 200 SKUs)
python data/synthetic_generators/generate_cli.py
```

## Registrar en el catálogo

Después de crear tu notebook, agrégalo a `config/notebooks_index.yml`:

```yaml
- id: "DS-06"
  title: "Demand Forecasting with ARIMA"
  specialty: "Data Science"
  process: "Plan"
  level: "Intermediate"
  tags: [forecast, arima, seasonality, demand]
  path: notebooks/30_data_science_ml/DS-06-demand_forecasting_arima.ipynb
  dataset_deps: [orders.csv, calendar.csv]
  estimated_time_min: 50
```

Luego actualiza la documentación:

```bash
# Actualizar navegación automática
python -m scripts update-navigation

# Exportar catálogo HTML
python -m scripts export-html
```

## Validar tu trabajo

Antes de hacer commit:

```bash
# 1. Validar metadatos y estructura
python -m scripts validate

# 2. Actualizar navegación
python -m scripts update-navigation

# 3. Exportar catálogo HTML
python -m scripts export-html

# 4. Ejecutar smoke test
python -m scripts smoke-test --ids <TU-ID>
```

## Checklist pre-commit

Antes de hacer commit, verifica:

- [ ] Notebook ejecutable sin errores (`python -m scripts catalog run <ID>`)
- [ ] Metadatos YAML completos en primera celda
- [ ] Registrado en `config/notebooks_index.yml`
- [ ] Validación exitosa (`python -m scripts validate`)
- [ ] Navegación actualizada (`python -m scripts update-navigation`)
- [ ] Datos sintéticos disponibles o generados internamente
- [ ] Comentarios útiles (no obvios)
- [ ] Visualizaciones claras con títulos
- [ ] Salida reproducible (mismo seed cada vez)
- [ ] Tiempo estimado realista en metadatos
- [ ] Objetivo es claro para líderes de supply chain
- [ ] Sin claves/secretos hardcodeadas (usar input interactivo o modo demo)

## Preguntas frecuentes

**¿Puedo usar datos reales?**  
No. Usa siempre datos sintéticos en `data/raw/`. Si necesitas incluir datasets nuevos, coordina con el mantenedor.

**¿Qué idioma uso?**  
Español preferente para líderes latam, pero comentarios en código pueden ser en inglés si es más claro.

**¿Cuántos notebooks puedo crear?**  
Los que necesites, pero prioriza:
1. Notebooks intro por especialidad (si no existen)
2. Notebooks que integren múltiples conceptos
3. Notebooks que resuelvan problemas reales de supply chain

**¿Cómo actualizo uno existente?**  
Modifica el notebook y actualiza metadatos. Si cambias nivel, duración o datasets, actualiza `notebooks_index.yml`.

## Contacto

Para preguntas o dudas:
- Abre una issue en GitHub
- Revisa notebooks existentes como referencia
- Ejecuta `python -m scripts.catalog search <palabra>` para encontrar ejemplos

---

**Gracias por contribuir a esta plataforma educativa para líderes de supply chain.** 🚀
