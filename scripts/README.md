# 🛠️ Scripts de Utilidades

Herramientas automatizadas para gestión, validación y mantenimiento de notebooks.

## 📋 Índice

- [CLI Unificado](#-cli-unificado)
- [Scripts Individuales](#-scripts-individuales)
- [Uso Común](#-uso-común)
- [Integración con CI/CD](#-integración-con-cicd)

---

## 🎯 CLI Unificado

El CLI principal proporciona acceso unificado a todas las utilidades.

### Instalación

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# Las dependencias ya están instaladas en el entorno
```

### Uso General

```bash
python -m scripts <comando> [opciones]
```

### Comandos Disponibles

#### 📚 **catalog** - Gestionar Catálogo

Navegar, buscar y ejecutar notebooks del catálogo.

```bash
# Listar todos los notebooks
python -m scripts catalog list

# Filtrar por especialidad
python -m scripts catalog list --specialty "Data Science"

# Filtrar por nivel
python -m scripts catalog list --level Intro

# Filtrar por tags
python -m scripts catalog list --tags eda,pandas

# Buscar por texto
python -m scripts catalog search "inventory"

# Mostrar detalles de un notebook
python -m scripts catalog show DS-01

# Ejecutar notebook(s)
python -m scripts catalog run DS-01
python -m scripts catalog run DS-01,DS-02 --timeout 600
```

#### ✅ **validate** - Validar Notebooks

Validar estructura y metadatos de notebooks.

```bash
# Validar todo (metadatos + estructura)
python -m scripts validate

# Solo metadatos
python -m scripts validate --type metadata

# Solo estructura
python -m scripts validate --type structure
```

#### 📄 **export-html** - Exportar Catálogo a HTML

Generar página HTML interactiva del catálogo.

```bash
# Exportar a ubicación por defecto (docs/catalog.html)
python -m scripts export-html

# Especificar ruta de salida
python -m scripts export-html --output /custom/path/catalog.html
```

#### 🧭 **update-navigation** - Actualizar Navegación

Actualizar sección de navegación en todos los notebooks con formato markdown legible.

```bash
# Actualizar navegación de todos los notebooks
python -m scripts update-navigation
```

#### 🧪 **smoke-test** - Tests Rápidos

Ejecutar tests rápidos de notebooks seleccionados.

```bash
# Ejecutar subset por defecto
python -m scripts smoke-test

# Especificar notebooks
python -m scripts smoke-test --ids DS-01,BA-01,OR-01

# Con timeout personalizado
python -m scripts smoke-test --ids DS-01 --timeout 600
```

#### 📦 **validate-reqs** - Validar Requirements

Validar consistencia de requirements.lock.

```bash
# Validar requirements
python -m scripts validate-reqs
```

---

## 📁 Scripts Individuales

Los scripts también pueden ejecutarse directamente cuando se necesita control más fino.

### 📊 catalog.py

**Propósito**: CLI para navegar y ejecutar notebooks del catálogo.

**Características**:
- Listar, buscar y filtrar notebooks
- Ejecutar notebooks con papermill
- Ver metadatos detallados

**Uso directo**:
```bash
python scripts/catalog.py list
python scripts/catalog.py run DS-01
```

### ✅ validate_notebook_metadata.py

**Propósito**: Validar que notebooks tengan metadatos completos y correctos.

**Verifica**:
- Presencia de campos requeridos (title, objective, level, etc.)
- Formato YAML válido en primera celda
- Coherencia con notebooks_index.yml

**Uso directo**:
```bash
python scripts/validate_notebook_metadata.py
python scripts/validate_notebook_metadata.py --fix
```

### 🏗️ validate_notebook_structure.py

**Propósito**: Validar estructura estándar de notebooks.

**Verifica**:
- Secciones requeridas (objetivos, conclusiones, operación)
- Ausencia de placeholders del template
- Estructura coherente

**Uso directo**:
```bash
python scripts/validate_notebook_structure.py
python scripts/validate_notebook_structure.py --output audit.csv
```

### 🔧 fix_notebook_metadata.py

**Propósito**: Corregir automáticamente problemas de metadatos.

**Correcciones**:
- Añadir bloques de metadatos faltantes
- Corregir tipos de celda incorrectos
- Formatear metadatos para legibilidad

**Uso directo**:
```bash
python scripts/fix_notebook_metadata.py
python scripts/fix_notebook_metadata.py --dry-run
```

### 📄 export_catalog_html.py

**Propósito**: Generar página HTML interactiva del catálogo.

**Características**:
- Tabla filtrable y buscable
- Agrupación por especialidad
- Enlaces directos a notebooks

**Uso directo**:
```bash
python scripts/export_catalog_html.py
python scripts/export_catalog_html.py --output custom.html
```

### 🧭 update_navigation.py

**Propósito**: Actualizar navegación entre notebooks con formato markdown legible.

**Características**:
- Enlaces anterior/siguiente automáticos con nombres completos de archivo
- Formato markdown simple y legible (sin HTML)
- Enlaces al índice del proyecto
- Respeta orden de notebooks_index.yml

**Uso directo**:
```bash
python scripts/update_navigation.py
```

### 🧪 smoke_test_notebooks.py

**Propósito**: Ejecutar tests rápidos con nbclient.

**Características**:
- Ejecución ligera sin dependencias externas
- Subset configurable de notebooks
- Detección rápida de errores de ejecución

**Uso directo**:
```bash
python scripts/smoke_test_notebooks.py
python scripts/smoke_test_notebooks.py --ids DS-01,BA-01
```

### 📦 validate_requirements.py

**Propósito**: Validar consistencia de archivos de dependencias.

**Verifica**:
- requirements.lock incluye todos los paquetes de requirements.txt
- Versiones consistentes
- Formato correcto

**Uso directo**:
```bash
python scripts/validate_requirements.py
```

---

## 💡 Uso Común

### Workflow de Desarrollo

#### 1. Crear Nuevo Notebook

```bash
# 1. Copiar template
cp notebooks/00_common/TEMPLATE.ipynb notebooks/30_data_science_ml/DS-08-new.ipynb

# 2. Editar y añadir al índice (config/notebooks_index.yml)

# 3. Actualizar navegación y catálogo
python -m scripts update-navigation
python -m scripts export-html

# 4. Validar
python -m scripts validate
```

#### 2. Mantenimiento del Proyecto

```bash
# Validar todo el proyecto
python -m scripts validate

# Actualizar navegación de notebooks
python -m scripts update-navigation

# Regenerar catálogo HTML
python -m scripts export-html

# Ejecutar smoke tests
python -m scripts smoke-test
```

#### 3. Exploración del Catálogo

```bash
# Ver notebooks de Data Science nivel Intro
python -m scripts catalog list --specialty "Data Science" --level Intro

# Buscar notebooks sobre inventario
python -m scripts catalog search inventory

# Ver detalles de un notebook
python -m scripts catalog show OR-01

# Ejecutar notebook
python -m scripts catalog run OR-01
```

---

## 🔄 Integración con CI/CD

### GitHub Actions

Ejemplo de workflow para validación automática:

```yaml
name: Validate Notebooks

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[core]
      
      - name: Validate metadata
        run: python -m scripts validate --type metadata
      
      - name: Validate structure
        run: python -m scripts validate --type structure
      
      - name: Validate requirements
        run: python -m scripts validate-reqs
      
      - name: Smoke test notebooks
        run: python -m scripts smoke-test --ids DS-01,BA-01,OR-01
```

### Pre-commit Hook

Añadir validación antes de commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash
python -m scripts validate --type metadata
if [ $? -ne 0 ]; then
    echo "❌ Validación de metadatos falló"
    exit 1
fi
```

---

## 📊 Estructura del Directorio

```
scripts/
├── __init__.py                     # Marca como paquete Python
├── __main__.py                     # Entry point (python -m scripts)
├── cli.py                          # CLI unificado principal
├── catalog.py                      # Gestión de catálogo
├── validate_notebook_metadata.py  # Validación de metadatos
├── validate_notebook_structure.py # Validación de estructura
├── export_catalog_html.py         # Exportar a HTML
├── update_navigation.py           # Actualizar navegación
├── smoke_test_notebooks.py        # Tests rápidos
├── validate_requirements.py       # Validar dependencias
└── README.md                      # Esta documentación
```

---

## 🎯 Buenas Prácticas

1. **Validar antes de commit**: Ejecutar `python -m scripts validate` antes de hacer commit
2. **Mantener navegación actualizada**: Después de añadir notebooks, ejecutar `update-navigation`
3. **Actualizar catálogo**: Regenerar HTML después de cambios mayores
4. **Smoke tests regulares**: Ejecutar antes de releases
5. **Documentar cambios**: Actualizar notebooks_index.yml con nueva información

---

## 🐛 Troubleshooting

### Error: "Module not found"

```bash
# Asegurar que el entorno virtual está activado
.\.venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -e .[core,notebooks]
```

### Error: "File not found" en validación

```bash
# Verificar que notebooks_index.yml está actualizado
python -m scripts catalog list
```

### Notebooks no ejecutan en smoke-test

```bash
# Verificar timeout (aumentar si es necesario)
python -m scripts smoke-test --timeout 600

# Ejecutar individual para ver error específico
python -m scripts catalog run <notebook-id>
```

---

## 📚 Referencias

- [notebooks_index.yml](../config/notebooks_index.yml) - Índice maestro de notebooks
- [catalog.html](../docs/catalog.html) - Catálogo HTML generado
- [README.md](../README.md) - Documentación principal del proyecto

---

**Última actualización**: Diciembre 2025
