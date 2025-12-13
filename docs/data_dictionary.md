# Data Dictionary

Diccionario de datos para los archivos CSV generados sintéticamente en `data/raw/`.

**Nota importante**: Estos archivos NO están incluidos en el repositorio (ver `.gitignore`). Se generan localmente mediante:
```bash
python data/synthetic_generators/generate_cli.py
```

**Volúmenes típicos** (con parámetros por defecto):
- **products.csv**: ~200 SKUs
- **locations.csv**: ~10-15 ubicaciones
- **orders.csv**: ~10,000-50,000 órdenes (90 días)
- **inventory.csv**: ~2,000-3,000 registros
- **transport_events.csv**: ~50,000+ eventos
- **calendar.csv**: 90-365 días

## products.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `sku` | string | Código único del producto (formato: SKU-XXXXX) |
| `category` | string | Categoría: Beverages, Snacks, PersonalCare, Household, Electronics |
| `brand` | string | Marca: BrandA, BrandB, BrandC, BrandD, BrandE |
| `unit_cost` | float | Costo unitario del producto (USD, rango: 5-150) |

**Registros generados:** conforme a scripts en `data/synthetic_generators/`

## locations.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `location_id` | string | Código único de ubicación (formato: LOC-XXX) |
| `type` | string | Tipo: Plant, DC (Distribution Center), Hub, Store |
| `region` | string | Región: NORTH, SOUTH, EAST, WEST, CENTER |
| `capacity` | integer | Capacidad de almacenamiento (unidades) |

**Registros generados:** conforme a scripts en `data/synthetic_generators/`

## calendar.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `date` | date | Fecha (formato: YYYY-MM-DD) |
| `is_holiday` | integer | 1 si es festivo, 0 si no (7% festivos) |
| `is_promo` | integer | 1 si hay promoción, 0 si no (15% días promocionales) |
| `day_of_week` | integer | Día de la semana (0=Lunes, 6=Domingo) |

**Rango típico:** definido por el generador en `generate_data.py`

## orders.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `order_id` | string | Identificador único de orden (formato: ORD-XXXXXX) |
| `date` | date | Fecha de la orden (formato: YYYY-MM-DD) |
| `sku` | string | SKU del producto ordenado |
| `qty` | integer | Cantidad ordenada (distribución gamma) |
| `location_id` | string | Ubicación de destino |
| `channel` | string | Canal de venta: Retail (50%), Ecom (30%), B2B (20%) |

**Volumen:** definido por parámetros del generador; incluye estacionalidad y promociones

## inventory.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `location_id` | string | Ubicación del inventario |
| `sku` | string | SKU del producto |
| `on_hand` | integer | Cantidad disponible en inventario (distribución gamma) |

**Volumen:** acorde al generador; proporciones pueden variar

## transport_events.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `event_id` | string | Identificador único del evento (formato: TEV-XXXXXX) |
| `order_id` | string | Orden asociada al evento |
| `status` | string | Estado: CREATED, DISPATCHED, IN_TRANSIT, DELIVERED, DELAYED |
| `lat` | float | Latitud del evento (rango: -33.6 a -33.2) |
| `lon` | float | Longitud del evento (rango: -70.8 a -70.5) |
| `timestamp` | datetime | Fecha y hora del evento |

**Volumen:** acorde al generador; número de eventos por orden puede variar

## gtfs_local.zip / gtfs_sample.zip (opcional)

Archivos estándar GTFS (General Transit Feed Specification) para pruebas de transporte masivo en `TR-01`.

| Archivo | Descripción | Ubicación |
|---------|-------------|-----------|
| `gtfs_local.zip` | Muestra local de GTFS para pruebas rápidas | `data/raw/` (no en repo) |
| `gtfs_sample.zip` | Paquete GTFS de ejemplo con rutas, trips y paradas | `data/raw/` (no en repo) |

**Uso:** Leídos por el notebook `notebooks/60_realtime_iot/TR-01-transporte_masivo.ipynb` usando librerías como `partridge` o `gtfs_kit`.

**Nota:** Estos archivos son opcionales. El notebook TR-01 puede funcionar sin ellos usando datos de muestra incluidos.

---

## Características de los Datos Sintéticos

Los datos generados incluyen:

✅ **Realismo**: Distribuciones estadísticas basadas en patrones reales del sector logístico  
✅ **Estacionalidad**: Picos en festivos y promociones  
✅ **Variabilidad**: Noise realista en demanda, delays, temperatura  
✅ **Reproducibilidad**: Generación con `--seed` para resultados idénticos  
✅ **Escalabilidad**: Parámetros configurables (días, SKUs, volumen)  

**No contienen información sensible o real**. Todos los valores son sintéticos.

---

**Generador**: `data/synthetic_generators/generate_data.py`  
**CLI**: `data/synthetic_generators/generate_cli.py`  
**Última actualización**: Diciembre 2025
