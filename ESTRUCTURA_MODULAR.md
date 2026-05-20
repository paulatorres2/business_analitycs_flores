# Estructura Modular del Proyecto

## Descripción General
El código ha sido reorganizado desde un archivo monolítico (`app.py`) a una estructura modular bien definida. Esto mejora:
- **Mantenibilidad**: Código más limpio y fácil de entender
- **Reusabilidad**: Módulos independientes que pueden usarse en otros proyectos
- **Testabilidad**: Funciones aisladas son más fáciles de probar
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin modificar código existente

## Estructura de Archivos

```
business_analitycs_flores/
├── app.py                 # Aplicación Flask principal (punto de entrada)
├── config.py              # Configuraciones y constantes
├── data_loader.py         # Carga y limpieza de datos
├── kpis.py                # Cálculos de KPIs
├── charts.py              # Generación de datos para gráficos
├── ml_models.py           # Modelos de Machine Learning
├── templates/             # Templates HTML
│   └── index.html
├── data/                  # Carpeta de datos
│   └── PROGRAMACIÓN Y CONTROL 2026.xlsx
└── venv/                  # Entorno virtual
```

## Módulos

### 1. **config.py**
Almacena todas las configuraciones y constantes globales:
- Rutas de archivos
- Columnas de defectos
- Columnas numéricas para conversión
- Columnas de texto para limpieza

**Uso:**
```python
from config import FILE_PATH, DEFECT_COLS
```

---

### 2. **data_loader.py**
Responsable de cargar y limpiar datos:
- `load_and_clean()`: Carga Excel, limpia, transforma y retorna DataFrame procesado

**Características:**
- Extrae headers automáticamente
- Conversión de tipos
- Creación de columnas derivadas (TOTAL_DEFECTOS, INDICE_CALIDAD, CUMPLIMIENTO, etc.)
- Documentado con docstrings

**Uso:**
```python
from data_loader import load_and_clean
DF = load_and_clean()
```

---

### 3. **kpis.py**
Cálculos de indicadores clave de desempeño:
- `calculate_kpis(df)`: KPIs principales (cumplimiento, exportación, calidad, etc.)
- `get_dataset_info(df)`: Información general del dataset
- `safe_float()`: Función auxiliar para manejo seguro de valores NaN

**Uso:**
```python
from kpis import calculate_kpis, get_dataset_info
kpis = calculate_kpis(DF)
info = get_dataset_info(DF)
```

---

### 4. **charts.py**
Generación de datos para visualizaciones:
- `top_suppliers_volume(df)`: Top 10 proveedores
- `top_defects(df)`: Ranking de defectos
- `supplier_deviation(df)`: Desviación de proveedores
- `weekly_trend(df)`: Tendencia semanal
- `quality_by_supplier(df)`: Calidad por proveedor
- `lugar_distribution(df)`: Distribución por lugar
- `estado_distribution(df)`: Distribución por estado
- `defects_over_weeks(df)`: Defectos por semana

**Uso:**
```python
from charts import top_suppliers_volume, top_defects
suppliers = top_suppliers_volume(DF)
defects = top_defects(DF)
```

---

### 5. **ml_models.py**
Modelos de Machine Learning:
- `predict_compliance(df)`: Random Forest para predicción de cumplimiento
- `cluster_suppliers(df)`: K-Means para clustering de proveedores
- `anomaly_detection(df)`: Isolation Forest para detección de anomalías
- `forecast_stems(df)`: Regresión Lineal para pronóstico de tallos

**Uso:**
```python
from ml_models import predict_compliance, cluster_suppliers
compliance = predict_compliance(DF)
clusters = cluster_suppliers(DF)
```

---

### 6. **app.py** (Aplicación Flask)
Punto de entrada principal que orquesta todos los módulos:
- Carga datos al iniciar
- Define rutas (endpoints) REST
- Importa funciones de los módulos especializados
- Retorna JSON con resultados

**Rutas disponibles:**
```
GET /                           → Página principal
GET /api/kpis                   → KPIs
GET /api/dataset-info           → Información del dataset
GET /api/charts/top-suppliers   → Top proveedores
GET /api/charts/top-defects     → Ranking defectos
GET /api/charts/supplier-deviation
GET /api/charts/weekly-trend
GET /api/charts/quality-by-supplier
GET /api/charts/lugar-distribution
GET /api/charts/estado-distribution
GET /api/charts/defects-over-weeks
GET /api/ml/compliance          → Predicción (Random Forest)
GET /api/ml/clusters            → Clustering (K-Means)
GET /api/ml/anomaly             → Anomalías (Isolation Forest)
GET /api/ml/forecast            → Pronóstico (Regresión Lineal)
```

---

## Flujo de Ejecución

1. **Al iniciar la aplicación:**
   ```
   app.py carga → data_loader.load_and_clean() → DF procesado
   ```

2. **Cuando se accede a un endpoint:**
   ```
   app.py (endpoint) → módulo correspondiente → JSON response
   ```

3. **Ejemplo - GET /api/kpis:**
   ```
   app.py → kpis.calculate_kpis(DF) → JSON
   ```

---

## Ventajas de esta Estructura

| Aspecto | Antes | Después |
|--------|--------|---------|
| **Líneas en app.py** | ~450 | ~120 |
| **Claridad** | Difícil de navegar | Cada módulo tiene un propósito claro |
| **Reutilización** | Código acoplado | Funciones independientes |
| **Testing** | Difícil aislar funciones | Fácil hacer unit tests |
| **Mantenimiento** | Bug en un lugar afecta todo | Cambios localizados |

---

## Cómo Agregar Nueva Funcionalidad

### Agregar un nuevo gráfico:
1. Agregar función en `charts.py`
2. Agregar ruta en `app.py`
3. Listo ✓

### Agregar un nuevo modelo ML:
1. Agregar función en `ml_models.py`
2. Agregar ruta en `app.py`
3. Listo ✓

### Cambiar configuración:
1. Modificar `config.py`
2. Los módulos ya importan de ahí
3. Listo ✓

---

## Próximos Pasos (Opcional)

- Agregar `tests/` para unit testing
- Agregar `requirements.txt` para dependencias
- Agregar `logging` para debugging
- Agregar validación de entrada en endpoints
- Agregar caché para datos que no cambian frecuentemente
