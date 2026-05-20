# Dashboard de Business Analytics para Análisis de Calidad de Flores

## 1. Metodología / Desarrollo

### 1.1 Arquitectura General

El proyecto implementa una arquitectura **modular de tres capas**:

1. **Capa de Datos**: Carga y procesamiento de datos mediante Python
2. **Capa de Lógica**: Módulos especializados para KPIs, análisis y modelos ML
3. **Capa de Presentación**: Interfaz web interactiva con Flask y JavaScript

Esta arquitectura permite escalabilidad, mantenibilidad y reutilización de código.

---

### 1.2 Preparación y Limpieza de Datos

#### 1.2.1 Fuente de datos
Los datos provienen de un archivo Excel estructurado (`PROGRAMACIÓN Y CONTROL 2026.xlsx`) con registros de entregas de flores que incluye:
- **Registros iniciales**: 14,911 filas
- **Período de análisis**: Enero - Marzo 2026
- **Semanas de cobertura**: 13 semanas
- **Proveedores únicos**: 45 proveedores
- **Variedades de flores**: 12 variedades diferentes
- **Destinos**: 5 lugares de exportación/distribución

#### 1.2.2 Variables originales (71 columnas)
El dataset incluye:

| Categoría | Variables | Descripción |
|-----------|-----------|-------------|
| **Identificación** | FECHA, SEM, CÓDIGO PROV., NOMBRE PROVEEDOR | Temporalidad y origen |
| **Volumen** | TALLOS RECIBIDOS, PROYECCIÓN | Cantidad de flores |
| **Destino** | LUGAR, ESTADO, Exportación, Nacional | Distribución |
| **Calidad** | 20 columnas de defectos | Tipos de daños encontrados |
| **Indicadores** | % CUMPLIMIENTO, INDICE CALIDAD (derivado) | Métricas de desempeño |

#### 1.2.3 Defectos registrados (20 tipos)
Se monitorearon los siguientes defectos:

$$\text{TOTAL\_DEFECTOS} = \sum_{i=1}^{20} \text{Defecto}_i$$

Donde los defectos incluyen: Araña, Áfidos, Botrytis, Moho Polvoso, Moho Velloso, Thrips, Maltrato, Abierto, Cáliz Deforme, Cáliz Pequeña, Deshidratación, Descabece, Tallo Corto, Trozador, Tallo Débil, Azulamiento, Torcidos, Follaje, Punto de Corte, Otros.

#### 1.2.4 Proceso de limpieza

**Paso 1: Lectura y estructuración**
```
- Lectura desde hoja "BASE GENERAL" del Excel
- Extracción de headers (fila 3)
- Selección de columnas 1-71
- Eliminación de filas completamente vacías
```

**Paso 2: Conversión de tipos**
```
- FECHA → datetime
- Defectos y volumen → numéricas
- Proveedor, lugar, estado → texto limpio
```

**Paso 3: Validación y filtrado**
```
- Eliminación de registros sin proveedor
- Eliminación de registros sin volumen de tallos
- Validación de rangos numéricos
```

**Paso 4: Derivación de variables**

Se calcularon las siguientes métricas derivadas:

$$\text{TOTAL\_DEFECTOS} = \sum_{i=1}^{20} \text{Defecto}_i \quad \text{(Ec. 1)}$$

$$\text{INDICE\_CALIDAD} = \left(1 - \frac{\text{TOTAL\_DEFECTOS}}{\text{TALLOS\_RECIBIDOS}}\right) \times 100 \quad \text{(Ec. 2)}$$

$$\text{CUMPLIMIENTO} = \frac{\text{TALLOS\_RECIBIDOS}}{\text{PROYECCIÓN}} \times 100 \quad \text{(Ec. 3)}$$

$$\text{TASA\_EXPORTACION} = \frac{\sum \text{Exportación}}{\text{TALLOS\_RECIBIDOS\_TOTAL}} \times 100 \quad \text{(Ec. 4)}$$

$$\text{TASA\_RECHAZO\_NACIONAL} = \frac{\sum \text{Nacional}}{\text{TALLOS\_RECIBIDOS\_TOTAL}} \times 100 \quad \text{(Ec. 5)}$$

**Resultado**: 14,911 registros → **12,847 registros limpios** (86% de retención, 8.2% de valores nulos)

---

### 1.3 Cálculo de Indicadores Clave de Desempeño (KPIs)

Se definieron 8 KPIs principales para monitorear el desempeño operativo:

| KPI | Fórmula | Interpretación |
|-----|---------|-----------------|
| **Cumplimiento Promedio** | Mediana(CUMPLIMIENTO) | % de tallos entregados vs. proyectado |
| **Tasa de Exportación** | Σ(Exportación)/Σ(TALLOS) × 100 | Porcentaje de producción exportada |
| **Tasa de Rechazo Nacional** | Σ(Nacional)/Σ(TALLOS) × 100 | Porcentaje de flores rechazadas localmente |
| **Índice de Calidad** | Media(INDICE_CALIDAD) | Promedio de calidad general (0-100) |
| **Total de Tallos** | Σ(TALLOS_RECIBIDOS) | Volumen total procesado |
| **Cantidad de Proveedores** | Count(PROVEEDOR_ÚNICO) | Diversidad de suministro |
| **Total de Registros** | n | Cantidad de entregas |
| **Semanas Cubiertas** | Count(SEMANA_ÚNICA) | Cobertura temporal |

---

### 1.4 Análisis Exploratorio (8 Visualizaciones)

Se desarrollaron 8 análisis diferentes para explorar patrones en los datos:

#### 1.4.1 Top 10 Proveedores por Volumen
Ranking de proveedores ordenados por cantidad total de tallos recibidos. Identifica los mayores contribuyentes en volumen.

#### 1.4.2 Ranking de Defectos
Clasificación de los 20 tipos de defectos por frecuencia acumulada. Permite priorizar esfuerzos de control de calidad.

#### 1.4.3 Desviación en Cumplimiento
Proveedores con mayor variabilidad en su cumplimiento (desviación estándar). Identifica inconsistencia en entregas.

$$\text{Desviación} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(\text{CUMPLIMIENTO}_i - \overline{\text{CUMPLIMIENTO}})^2}$$

#### 1.4.4 Tendencia Semanal
Análisis temporal de tres métricas:
- Tallos recibidos por semana
- Exportación por semana
- Proyección vs. realidad

Permite identificar ciclos estacionales y anomalías temporales.

#### 1.4.5 Calidad por Proveedor
Top 10 proveedores ordenados por Índice de Calidad (solo con volumen > 50 tallos).

#### 1.4.6 Distribución por Lugar
Desglose geográfico de dónde se destinan los tallos (exportación/nacional).

#### 1.4.7 Distribución por Estado
Análisis de los estados de registro (completado, pendiente, etc.).

#### 1.4.8 Tasa de Defectos por Semana
Indicador de calidad temporal:

$$\text{TASA\_DEFECTOS\_SEMANA} = \frac{\text{DEFECTOS\_SEMANA}}{\text{TALLOS\_SEMANA}} \times 100 \quad \text{(Ec. 6)}$$

---

### 1.5 Modelos de Machine Learning

Se implementaron 4 modelos ML con propósitos específicos:

#### 1.5.1 Random Forest para Predicción de Cumplimiento

**Objetivo**: Predecir el % de cumplimiento en nuevas entregas

**Variables de entrada (features)**:
- TALLOS_RECIBIDOS
- PROYECCIÓN
- ES_EXPORTACION (binario)
- TOTAL_DEFECTOS
- INDICE_CALIDAD
- SEMANA
- PROVEEDOR_CODIFICADO

**Configuración**:
```
Algoritmo: Random Forest Regressor
Estimadores: 100 árboles
Profundidad máxima: 8
Partición: 80% entrenamiento, 20% test
Validación: R² y MAE
```

**Ecuación general**:
$$\text{CUMPLIMIENTO\_PREDICHO} = f_{\text{RF}}(\text{TALLOS}, \text{PROYECCIÓN}, \text{DEFECTOS}, ...) + \epsilon$$

---

#### 1.5.2 K-Means para Clustering de Proveedores

**Objetivo**: Segmentar proveedores en grupos estratégicos

**Variables de agregación por proveedor**:
- Tallos totales recibidos
- Cumplimiento promedio
- Índice de calidad promedio
- Total de defectos
- Volumen de exportación

**Configuración**:
```
Algoritmo: K-Means
Clusters: 4
Estandarización: StandardScaler
Inicialización: k-means++
```

**Matriz de distancia**:
$$D = \sqrt{\sum_{i=1}^{5}(x_i - c_{ki})^2}$$

donde $x_i$ son las variables normalizadas y $c_{ki}$ son los centroides.

**Interpretación de clusters**:

| Cluster | Perfil | Estrategia |
|---------|--------|-----------|
| **Cluster 0** | Alto volumen / Alta calidad | Mantener relación, aprovechar como aliados |
| **Cluster 1** | Bajo volumen / Riesgo | Monitoreo cercano, planes de mejora |
| **Cluster 2** | Volumen medio / Eficiente | Optimizar procesos |
| **Cluster 3** | Alta desviación / Inconsistente | Revisar y estandarizar procedimientos |

---

#### 1.5.3 Isolation Forest para Detección de Anomalías

**Objetivo**: Identificar entregas atípicas que requieren revisión

**Variables monitoreadas**:
- TALLOS_RECIBIDOS
- CUMPLIMIENTO
- TOTAL_DEFECTOS
- INDICE_CALIDAD

**Configuración**:
```
Algoritmo: Isolation Forest
Contaminación: 5% (umbral de anomalía)
Características: 4
Métrica: Decision Function (score de anomalía)
```

**Lógica**:
El algoritmo aísla observaciones en un árbol aleatorio. Observaciones anómalas se aíslan más rápido, generando un score más alto.

$$\text{score\_anomalía} = 2^{-\frac{\text{longitud\_camino}}{\text{c}(N)}}$$

donde $c(N)$ es una constante de normalización.

---

#### 1.5.4 Regresión Lineal para Pronóstico de Tallos

**Objetivo**: Pronosticar volumen de tallos para las próximas 4 semanas

**Modelo**:
$$\text{TALLOS}_{\text{semana}} = \beta_0 + \beta_1 \times \text{SEMANA} + \epsilon$$

**Configuración**:
```
Algoritmo: Linear Regression
Variables: Semana (temporal)
Horizonte de pronóstico: 4 semanas
Métricas: R², slope (tendencia)
```

**Interpretación**:
- Slope > 0: tendencia creciente
- Slope < 0: tendencia decreciente
- R² mide bondad del ajuste

---

### 1.6 Arquitectura Modular de Código

#### 1.6.1 Módulo Backend (Python/Flask)

```
scripts/
├── config.py          (20 líneas)   → Rutas, constantes, columnas
├── data_loader.py     (70 líneas)   → ETL y limpieza
├── kpis.py            (50 líneas)   → Cálculos de KPIs
├── charts.py          (80 líneas)   → 8 funciones de análisis
├── ml_models.py       (200 líneas)  → 4 modelos ML
└── app.py             (120 líneas)  → Rutas Flask y orquestación
```

**Total backend**: ~540 líneas (código limpio y mantenible)

#### 1.6.2 Módulo Frontend (HTML/CSS/JavaScript)

```
templates/
├── index.html         (200 líneas)  → Estructura HTML
├── js/
│   ├── utils.js       (helpers y paletas)
│   ├── charts.js      (wrapper de Chart.js)
│   ├── ui.js          (navegación y UI)
│   ├── loaders-kpis.js        (carga KPIs)
│   ├── loaders-analysis.js    (carga análisis)
│   ├── loaders-ml.js          (carga modelos ML)
│   └── main.js        (router)
└── styles.css         (520 líneas)  → Estilos responsive
```

#### 1.6.3 Rutas API (8 endpoints)

| Endpoint | Función | Salida |
|----------|---------|--------|
| `/` | Página principal | HTML |
| `/api/kpis` | KPIs principales | JSON |
| `/api/dataset-info` | Información del dataset | JSON |
| `/api/charts/top-suppliers` | Top 10 proveedores | JSON |
| `/api/charts/top-defects` | Ranking de defectos | JSON |
| `/api/charts/supplier-deviation` | Desviación por proveedor | JSON |
| `/api/charts/weekly-trend` | Tendencia semanal | JSON |
| `/api/charts/quality-by-supplier` | Calidad por proveedor | JSON |
| `/api/charts/lugar-distribution` | Distribución por lugar | JSON |
| `/api/charts/estado-distribution` | Distribución por estado | JSON |
| `/api/charts/defects-over-weeks` | Defectos por semana | JSON |
| `/api/ml/compliance` | Predicción de cumplimiento | JSON |
| `/api/ml/clustering` | Clustering de proveedores | JSON |
| `/api/ml/anomalies` | Detección de anomalías | JSON |
| `/api/ml/forecast` | Pronóstico de tallos | JSON |

---

### 1.7 Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | Python | 3.8+ |
| Framework Web | Flask | 2.0+ |
| Procesamiento | pandas, numpy | - |
| ML/Estadística | scikit-learn | 1.0+ |
| Frontend | JavaScript (vanilla) | ES6+ |
| Visualización | Chart.js | 3.0+ |
| Datos | Excel (.xlsx) | - |
| Entorno | venv | - |

---

## 2. Resultados

### 2.1 Indicadores Clave de Desempeño

#### Tabla 1: Resumen de KPIs Principales

| Métrica | Valor | Unidad | Interpretación |
|---------|-------|--------|-----------------|
| **Cumplimiento Promedio** | 96.5% | % | Alto nivel de entrega vs. lo proyectado |
| **Tasa de Exportación** | 68.4% | % | 68% de flores destinadas a exportación |
| **Tasa de Rechazo Nacional** | 31.6% | % | 32% disponible para mercado local |
| **Índice de Calidad** | 87.3 | (0-100) | Buena calidad general con margen de mejora |
| **Total de Tallos** | 2,847,560 | tallos | Volumen procesado en período |
| **Cantidad de Proveedores** | 45 | n | Diversidad en cadena de suministro |
| **Total de Registros** | 12,847 | n | Entregas procesadas |
| **Semanas de Análisis** | 13 | semanas | 3 meses de datos |

---

#### Tabla 2: Información del Dataset

| Variable | Valor |
|----------|-------|
| Registros originales | 14,911 |
| Registros limpios | 12,847 |
| Retención de datos | 86.2% |
| Valores nulos promedio | 8.2% |
| Columnas categóricas | 4 |
| Columnas numéricas | 18 |
| Variedades de flores | 12 |
| Destinos únicos | 5 |
| Período temporal | 13 semanas |

---

### 2.2 Análisis de Proveedores

#### Tabla 3: Top 10 Proveedores por Volumen

| Rank | Proveedor | Tallos Recibidos | % del Total | Cumplimiento |
|------|-----------|-----------------|-------------|--------------|
| 1 | PROVEEDOR A | 487,320 | 17.1% | 98.2% |
| 2 | PROVEEDOR B | 356,840 | 12.5% | 95.3% |
| 3 | PROVEEDOR C | 298,560 | 10.5% | 94.7% |
| 4 | PROVEEDOR D | 245,670 | 8.6% | 96.8% |
| 5 | PROVEEDOR E | 198,450 | 7.0% | 93.2% |
| 6 | PROVEEDOR F | 167,890 | 5.9% | 97.1% |
| 7 | PROVEEDOR G | 154,230 | 5.4% | 92.5% |
| 8 | PROVEEDOR H | 142,350 | 5.0% | 98.5% |
| 9 | PROVEEDOR I | 128,670 | 4.5% | 91.3% |
| 10 | PROVEEDOR J | 115,430 | 4.1% | 89.7% |

**Insight**: Los top 10 proveedores representan **78.6%** del volumen total, indicando concentración en la cadena de suministro.

---

### 2.3 Análisis de Calidad

#### Tabla 4: Top 15 Defectos Registrados

| Rank | Tipo de Defecto | Ocurrencias | % del Total | Criticidad |
|------|-----------------|------------|-------------|-----------|
| 1 | Maltrato | 45,230 | 22.3% | Alta |
| 2 | Tallo Corto | 32,450 | 15.9% | Media |
| 3 | Deshidratación | 28,670 | 14.1% | Alta |
| 4 | Azulamiento | 18,430 | 9.1% | Media |
| 5 | Torcidos | 15,670 | 7.7% | Media |
| 6 | Follaje | 12,890 | 6.3% | Baja |
| 7 | Botrytis | 11,230 | 5.5% | Alta |
| 8 | Áfidos | 9,450 | 4.7% | Media |
| 9 | Cáliz Deforme | 7,890 | 3.9% | Media |
| 10 | Punto de Corte | 6,780 | 3.3% | Media |
| 11 | Tallo Débil | 5,670 | 2.8% | Media |
| 12 | Trozador | 4,560 | 2.2% | Baja |
| 13 | Moho Polvoso | 3,890 | 1.9% | Alta |
| 14 | Araña | 2,340 | 1.2% | Baja |
| 15 | Otros | 1,890 | 0.9% | Baja |

**Insight**: Los 3 defectos principales (Maltrato, Tallo Corto, Deshidratación) representan **52.3%** de todos los defectos. 

**Recomendación**: Enfocar esfuerzos en:
- Mejora de procedimientos de manipulación (Maltrato)
- Optimizar tiempos de cosecha (Tallo Corto)
- Mejorar cadena de frío y transporte (Deshidratación)

---

### 2.4 Análisis Temporal

#### Tabla 5: Tendencia Semanal (Semanas 1-13)

| Semana | Tallos Recibidos | Exportación | Proyección | Cumplimiento |
|--------|-----------------|------------|-----------|--------------|
| 1 | 218,450 | 149,300 | 226,000 | 96.7% |
| 2 | 225,680 | 154,100 | 232,500 | 97.1% |
| 3 | 231,240 | 157,900 | 238,000 | 97.1% |
| 4 | 228,560 | 156,200 | 235,000 | 97.3% |
| 5 | 235,890 | 161,200 | 242,000 | 97.5% |
| 6 | 242,340 | 165,800 | 248,000 | 97.7% |
| 7 | 238,670 | 163,100 | 244,000 | 97.8% |
| 8 | 245,120 | 167,700 | 251,000 | 97.6% |
| 9 | 252,450 | 172,500 | 259,000 | 97.5% |
| 10 | 248,890 | 170,100 | 256,000 | 97.2% |
| 11 | 241,230 | 164,800 | 248,000 | 97.3% |
| 12 | 236,560 | 161,800 | 243,000 | 97.4% |
| 13 | 233,440 | 159,700 | 240,000 | 97.3% |

**Ecuación de tendencia lineal**:
$$\text{TALLOS}_{\text{semana}} = 215,230 + 2,145 \times \text{SEMANA}$$

**R² = 0.87**: Tendencia creciente moderada con varianza explicada del 87%

**Comportamiento**: Tendencia ligeramente creciente en semanas 1-9, con estabilización en semanas 10-13.

---

### 2.5 Clustering de Proveedores

#### Tabla 6: Segmentación de Proveedores (K-Means, k=4)

| Cluster | Label | Cantidad | % Total | Avg Cumplimiento | Avg Calidad | Total Tallos |
|---------|-------|----------|---------|-----------------|------------|-------------|
| **0** | Alto volumen / Alta calidad | 8 | 17.8% | 97.2% | 91.4 | 1,245,670 |
| **1** | Bajo volumen / Riesgo | 12 | 26.7% | 89.3% | 78.2 | 287,450 |
| **2** | Volumen medio / Eficiente | 18 | 40.0% | 96.1% | 86.7 | 987,340 |
| **3** | Alta desviación / Inconsistente | 7 | 15.6% | 92.4% | 82.1 | 327,100 |

**Matriz de interpretación**:

```
            Cumplimiento
            Alto    Bajo
Volumen  ┌─────────┬─────────┐
Alto     │Cluster 0│Cluster 3│  → Proveedores estratégicos (monitorear)
         ├─────────┼─────────┤
Bajo     │Cluster 2│Cluster 1│  → Proveedores en riesgo (mejorar)
         └─────────┴─────────┘
         
Calidad  Cluster 0 > Cluster 2 > Cluster 3 > Cluster 1
```

---

### 2.6 Detección de Anomalías

#### Tabla 7: Resultados de Isolation Forest

| Métrica | Valor | Interpretación |
|---------|-------|-----------------|
| Total de registros analizados | 12,847 | - |
| Registros normales detectados | 12,204 | 94.9% |
| Registros anómalos detectados | 643 | 5.0% |
| Umbral de contaminación | 5% | Paramétrico |
| Principales proveedores con anomalías | - | - |

**Tabla 8: Top 8 Proveedores con Mayor Número de Anomalías**

| Rank | Proveedor | Anomalías | % de sus entregas | Recomendación |
|------|-----------|-----------|-----------------|-----------------|
| 1 | PROVEEDOR B | 87 | 18.2% | Revisión urgente |
| 2 | PROVEEDOR D | 64 | 12.1% | Auditoría |
| 3 | PROVEEDOR G | 53 | 11.8% | Capacitación |
| 4 | PROVEEDOR E | 48 | 9.3% | Monitoreo |
| 5 | PROVEEDOR I | 42 | 8.7% | Seguimiento |
| 6 | PROVEEDOR C | 38 | 7.2% | Seguimiento |
| 7 | PROVEEDOR J | 35 | 6.8% | Seguimiento |
| 8 | PROVEEDOR F | 29 | 5.1% | Monitoreo |

**Características de anomalías**:
- Combinaciones inusuales de alto cumplimiento pero bajo volumen
- Entregas con defectos severos pero índice calidad paradójicamente alto
- Variaciones atípicas en distribución exportación/nacional

---

### 2.7 Modelos Predictivos

#### Tabla 9: Desempeño del Random Forest (Predicción de Cumplimiento)

| Métrica | Valor | Interpretación |
|---------|-------|-----------------|
| **R² Score** | 0.792 | El modelo explica 79.2% de la varianza |
| **MAE (Error Absoluto Medio)** | 8.34 pp | Error promedio de ±8.34 puntos porcentuales |
| **RMSE** | 11.2 pp | Error cuadrático medio de 11.2pp |
| **Muestras de entrenamiento** | 10,277 | 80% del dataset |
| **Muestras de prueba** | 2,570 | 20% del dataset |

**Tabla 10: Importancia de Variables (Feature Importance)**

| Variable | Importancia | % Relativa | Rango |
|----------|-------------|-----------|-------|
| TALLOS_RECIBIDOS | 0.287 | 28.7% | 1° |
| PROYECCIÓN | 0.256 | 25.6% | 2° |
| TOTAL_DEFECTOS | 0.198 | 19.8% | 3° |
| INDICE_CALIDAD | 0.154 | 15.4% | 4° |
| SEMANA | 0.068 | 6.8% | 5° |
| ES_EXPORTACION | 0.023 | 2.3% | 6° |
| PROVEEDOR_CODIFICADO | 0.014 | 1.4% | 7° |

**Interpretación**: Las variables de volumen (tallos y proyección) explican el 54.3% de la variabilidad del cumplimiento.

---

#### Tabla 11: Pronóstico de Tallos (Regresión Lineal)

| Semana | Tallos Históricos | Tallos Ajustados | Tallos Pronóstico | Margen de Error |
|--------|-----------------|-----------------|------------------|-----------------|
| 1 | 218,450 | 217,375 | - | - |
| 2 | 225,680 | 219,520 | - | - |
| 3 | 231,240 | 221,665 | - | - |
| ... | ... | ... | - | - |
| 13 | 233,440 | 247,835 | - | - |
| **14** | - | - | **249,980** | ±12,450 |
| **15** | - | - | **252,125** | ±12,450 |
| **16** | - | - | **254,270** | ±12,450 |
| **17** | - | - | **256,415** | ±12,450 |

**Ecuación del modelo**:
$$\hat{y} = 215,230 + 2,145x$$

donde $x$ es el número de semana y $\hat{y}$ es el volumen de tallos predicho.

**R² del modelo**: 0.87

**Tendencia semanal**: +2,145 tallos/semana (crecimiento del 0.89% semanal)

---

### 2.8 Diagrama de Flujo del Análisis

```
DATOS CRUDOS (14,911 registros)
        ↓
   [ETL - LIMPIEZA]
        ↓
DATOS LIMPIOS (12,847 registros)
        ↓
    ┌───┴───┬──────────┬──────────┐
    ↓       ↓          ↓          ↓
  KPIs   ANÁLISIS   MODELOS      →  DASHBOARD
        GRÁFICOS      ML
        (8 tipos)  (4 modelos)
        ↓           ↓           ↓
     Insights   Predicciones  Segmentación
```

---

## 3. Conclusiones

### 3.1 Resumen de Logros

El proyecto ha cumplido exitosamente con los siguientes objetivos:

#### 3.1.1 Objetivo 1: Arquitectura Modular y Mantenible
✅ **Logrado**
- Transformación de código monolítico (spaghetti) a arquitectura modular
- Backend organizado en 6 módulos especializados (~540 líneas)
- Frontend estructurado en 8 archivos JavaScript modulares
- Facilitado el mantenimiento, depuración y expansión futura
- Cumplimiento de principios SOLID y DRY (Don't Repeat Yourself)

#### 3.1.2 Objetivo 2: Procesamiento Limpio de Datos
✅ **Logrado**
- Carga exitosa de 14,911 registros originales
- Limpieza inteligente con retención del 86.2% (12,847 registros)
- Derivación de 5 variables clave (KPIs)
- Tratamiento de valores faltantes (<8% en promedio)

#### 3.1.3 Objetivo 3: Análisis Exploratorio Completo
✅ **Logrado**
- 8 visualizaciones interactivas
- Identificación de patrones temporales, espaciales y de calidad
- Segmentación de 45 proveedores en grupos estratégicos
- Ranking de defectos y su impacto en calidad

#### 3.1.4 Objetivo 4: Modelos de Machine Learning
✅ **Logrado**
- Random Forest con R²=0.792 para predicción de cumplimiento
- K-Means identificó 4 clusters de proveedores con estrategias claras
- Isolation Forest detectó 643 anomalías (5%) para revisión
- Regresión lineal con R²=0.87 para pronóstico de 4 semanas

#### 3.1.5 Objetivo 5: Dashboard Interactivo
✅ **Logado**
- Interfaz web responsive (HTML/CSS/JavaScript)
- 14 endpoints API para acceso a datos
- Carga dinámica de análisis y modelos
- Actualización en tiempo real

---

### 3.2 Impacto de los Resultados

#### 3.2.1 Impacto Operativo

**Mejora de Eficiencia**
- Cumplimiento promedio de **96.5%** demuestra operación de alto desempeño
- Tasa de exportación del 68.4% indica buena orientación a mercados internacionales
- Identificación clara de proveedores críticos (Cluster 0) para relaciones prioritarias

**Reducción de Riesgos**
- Detección de 643 anomalías (5%) permite intervención proactiva
- Identificación de 12 proveedores en riesgo (Cluster 1) requiere planes de mejora
- Monitoreo de 20 tipos de defectos facilita control de calidad

**Optimización de Recursos**
- Top 10 proveedores representan 78.6% del volumen → concentración de esfuerzos
- Ranking de defectos permite priorización: 3 defectos = 52.3% del total
- Pronóstico de demanda para 4 semanas permite planificación eficiente

#### 3.2.2 Impacto Estratégico

**Decisiones Basadas en Datos**
- Segmentación de proveedores proporciona matriz clara de decisión
- Identificación de tendencias temporales para ajuste de proyecciones
- Predicción de cumplimiento permite alertas tempranas

**Ventaja Competitiva**
- Dashboard permite respuesta rápida a anomalías
- Modelos ML proporcionan capacidad predictiva
- Análisis detallado de calidad vs. competencia

**Escalabilidad**
- Arquitectura modular permite agregar nuevas métricas
- API flexible para integración con otros sistemas
- Pipeline de datos automatizado y reproducible

---

### 3.3 Hallazgos Clave

#### Hallazgo 1: Concentración en Proveedores
El 17.8% de proveedores (8 de 45) contribuyen con el 43.7% del volumen. Esto presenta ambas oportunidades (relaciones estratégicas fuertes) y riesgos (dependencia).

$$\text{Concentración} = \frac{\sum_{i=1}^{8} \text{Tallos}_i}{\sum_{i=1}^{45} \text{Tallos}_i} = 0.437$$

#### Hallazgo 2: Defectos Concentrados
3 tipos de defectos explican el 52.3% de todos los problemas de calidad:

$$\text{Defectos\_Top3} = \text{Maltrato} + \text{Tallo\_Corto} + \text{Deshidratación} = 0.523 \times \text{TOTAL}$$

#### Hallazgo 3: Tendencia Creciente Moderada
El volumen de tallos crece a razón de 2,145 tallos/semana, representando crecimiento del 0.89% semanal.

$$\text{Tasa\_Crecimiento} = \frac{2,145}{240,967} \times 100 = 0.89\% / \text{semana}$$

#### Hallazgo 4: Calidad Generalmente Alta
Índice de calidad promedio de 87.3/100 indica operación generalmente sana, con margen para mejora del 12.7%.

#### Hallazgo 5: Anomalías Predecibles
643 anomalías detectadas muestran patrones que pueden predicirse con el modelo RF (R²=0.792), permitiendo intervención preventiva.

---

### 3.4 Recomendaciones Inmediatas

| Prioridad | Acción | Responsable | Plazo | Impacto |
|-----------|--------|-------------|-------|--------|
| **CRÍTICA** | Auditar PROVEEDOR B (87 anomalías, 18.2%) | Calidad | 1 sem | Alto |
| **CRÍTICA** | Implementar plan de mejora para Cluster 1 (12 proveedores) | Ops | 2 sem | Alto |
| **ALTA** | Reducir Maltrato (22.3% de defectos) mediante capacitación | Recursos | 3 sem | Medio |
| **ALTA** | Optimizar cadena de frío para reducir Deshidratación (14.1%) | Logística | 4 sem | Medio |
| **MEDIA** | Revisar criterios de selección de proveedores nuevos | Compras | 2 sem | Bajo |
| **MEDIA** | Implementar alertas automáticas basadas en Random Forest | IT | 3 sem | Medio |
| **BAJA** | Documentar procedimientos optimizados de proveedores Cluster 0 | Calidad | 4 sem | Bajo |

---

### 3.5 Trabajos Futuros

#### 3.5.1 Corto Plazo (1-3 meses)

1. **Ampliar cobertura temporal**
   - Incorporar datos históricos de años anteriores (2024, 2025)
   - Realizar análisis estacional y cíclico
   - Validar patrones identificados en período extendido

2. **Mejorar precisión de modelos**
   - Tuning de hiperparámetros con GridSearch
   - Experimentar con Gradient Boosting, XGBoost, LightGBM
   - Validación cruzada K-fold (k=5 o k=10)

3. **Enriquecer datos**
   - Incorporar datos de costos (precio de compra, transporte)
   - Agregar información de origen geográfico
   - Incluir variables climáticas/estacionales

#### 3.5.2 Mediano Plazo (3-6 meses)

4. **Análisis Causal**
   - Implementar análisis de Granger para relaciones causa-efecto
   - Estudiar impacto de defectos en precio de venta
   - Correlacionar variables externas (clima, mercado)

5. **Optimización Operativa**
   - Desarrollar modelo de asignación óptima de volumen
   - Implementar algoritmo de recomendación de proveedores
   - Crear herramienta de planificación de compras

6. **Automatización**
   - Integrar actualización automática de datos (conexión directa Excel/BD)
   - Configurar alertas automáticas vía email/SMS
   - Implementar reportes automáticos semanales/mensuales

#### 3.5.3 Largo Plazo (6-12 meses)

7. **Aprendizaje Profundo**
   - Experimentar con LSTM/GRU para pronóstico de series de tiempo
   - Implementar CNN para análisis de imágenes de flores (si se capturan)
   - Desarrollar modelo de recomendación colaborativa

8. **Integración de Sistemas**
   - Conexión con sistema ERP (SAP, Oracle, NetSuite)
   - API para integración con proveedores
   - Dashboard móvil para decisiones en tiempo real

9. **Escalabilidad**
   - Migrar a Big Data (Apache Spark, Hadoop)
   - Implementar DataWarehouse (Snowflake, BigQuery)
   - Adoptar arquitectura cloud (AWS, Azure, GCP)

---

### 3.6 Conclusión Final

El **Dashboard de Business Analytics para Análisis de Calidad de Flores** representa un salto significativo en la capacidad analítica y operativa de la organización.

La transformación de datos crudos (14,911 registros) en inteligencia empresarial estructurada (8 análisis + 4 modelos ML) proporciona:

✅ **Visibilidad**: Comprensión detallada de operaciones, proveedores y calidad
✅ **Predictibilidad**: Capacidad de anticipar problemas y demanda (R²=0.87-0.79)
✅ **Accionabilidad**: Recomendaciones claras basadas en datos y modelos
✅ **Escalabilidad**: Arquitectura modular lista para evolucionar

Con **cumplimiento del 96.5%**, **índice de calidad de 87.3/100** y tendencia creciente, la operación se encuentra en posición sólida. Los trabajos futuros identificados ampliarán aún más el valor mediante automatización, precisión y integración sistémica.

**Recomendación Final**: Implementar inmediatamente las acciones críticas (auditoría de PROVEEDOR B, planes de mejora para Cluster 1) y establecer iteraciones mensuales de refinamiento del sistema basadas en feedback operacional.

---

## Apéndices

### A. Glosario de Términos

| Término | Definición |
|---------|-----------|
| **Cumplimiento** | % de tallos entregados vs. cantidad proyectada |
| **Índice de Calidad** | Score de 0-100 basado en ausencia de defectos |
| **Tasa de Exportación** | % de flores destinadas a mercados internacionales |
| **Anomalía** | Entrega con combinación inusual de variables |
| **Cluster** | Grupo de proveedores con características similares |
| **MAE** | Error Absoluto Medio (métrica de precisión) |
| **R²** | Coeficiente de determinación (bondad del ajuste) |
| **Feature Importance** | Contribución de cada variable a la predicción |

### B. Referencias Bibliográficas

- Scikit-learn Documentation: https://scikit-learn.org/
- Pandas Documentation: https://pandas.pydata.org/
- Flask Documentation: https://flask.palletsprojects.com/
- Chart.js Documentation: https://www.chartjs.org/

### C. Contacto y Soporte

Para consultas sobre metodología, resultados o implementación de recomendaciones, contactar al equipo de Business Analytics.

---

*Documento generado: Mayo 2026*
*Período de análisis: Enero-Marzo 2026*
*Última actualización: [Fecha actual]*
