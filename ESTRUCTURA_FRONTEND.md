# Estructura Modular del Frontend (HTML/CSS/JS)

## Descripción General

El `index.html` original con ~900 líneas (CSS inline + JavaScript inline) ha sido reorganizado en módulos separados. Esto garantiza:

- **Separación de responsabilidades**: CSS, HTML y JavaScript en archivos dedicados
- **Facilidad de mantenimiento**: Cambios localizados sin afectar otras partes
- **Rendimiento**: Mejor cacheo del navegador
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

## Estructura de Archivos

```
templates/
├── index.html              # Punto de entrada (HTML limpio)
├── styles.css              # Todos los estilos CSS
├── js/
│   ├── utils.js            # Utilidades y helpers
│   ├── charts.js           # Manejo de Chart.js
│   ├── ui.js               # Navegación y UI
│   ├── loaders-kpis.js     # Carga de KPIs y dataset
│   ├── loaders-analysis.js # Carga de gráficos de análisis
│   ├── loaders-ml.js       # Carga de modelos ML
│   └── main.js             # Inicialización
```

## Archivos Detallados

### 1. **index.html** (Limpio)
- Solo estructura HTML semántica
- Referencias a CSS y JS externos
- Sin estilos ni scripts inline
- **Tamaño**: ~200 líneas vs 900 originales

**Headers importantes:**
```html
<link rel="stylesheet" href="styles.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
```

**Scripts al final (orden importante):**
```html
<script src="js/utils.js"></script>
<script src="js/charts.js"></script>
<script src="js/ui.js"></script>
<script src="js/loaders-kpis.js"></script>
<script src="js/loaders-analysis.js"></script>
<script src="js/loaders-ml.js"></script>
<script src="js/main.js"></script>
```

---

### 2. **styles.css** (Todo el diseño)
Contiene:
- **Variables CSS**: Paleta de colores, dimensiones, sombras
- **Reset**: Box-sizing, márgenes, padding
- **Componentes**: Sidebar, topbar, cards, grillas
- **Utilidades**: Spinners, badges, pills
- **Responsivo**: Media queries para mobile
- **Animaciones**: Spin, hover effects

**Organización:**
```css
/* ── DESIGN TOKENS & RESET ── */
/* ── SIDEBAR ── */
/* ── MAIN CONTENT ── */
/* ── PAGES ── */
/* ── CHART GRID ── */
/* ── ML SECTION ── */
/* ── RESPONSIVE DESIGN ── */
```

---

### 3. **js/utils.js** (Utilidades)
Funciones base reutilizables:

- `PALETTE`: Array de colores para gráficos
- `gridColor`: Color de grillas
- `get(url)`: Fetch helper async
- `fmt(n, suffix)`: Formatea números con locale español
- `deepMerge(a, b)`: Merge recursivo para options de Chart.js

**Uso:**
```javascript
const data = await get('/api/kpis');
const formatted = fmt(1234.5, '%');  // "1.234,5%"
```

---

### 4. **js/charts.js** (Chart.js Helper)
Una función principal:

- `mkChart(id, type, data, options)`: Crea/actualiza gráficos
  - Destruye gráfico anterior si existe
  - Aplica opciones por defecto
  - Merge inteligente de opciones

**Uso:**
```javascript
mkChart('chart-weekly', 'line', {
  labels: semanas,
  datasets: [{ label: 'Tallos', data: tallos }]
});
```

---

### 5. **js/ui.js** (Navegación)
Lógica de UI e interacción:

- `pages`: Array de nombres de páginas
- `initializedPages`, `mlLoaded`: Flags de caché
- `showPage(name)`: Cambia página y carga si es primera vez
- `showMLPanel(name)`: Cambia panel ML y carga modelo

**Uso:**
```html
<a onclick="showPage('kpis')">KPIs</a>
<div class="ml-tab" onclick="showMLPanel('compliance')">Compliance</div>
```

---

### 6. **js/loaders-kpis.js** (KPIs & Dataset)
Carga de datos principales:

- `loadKPIs()`: Obtiene `/api/kpis`, renderiza topbar y grid de KPIs
- `loadDatasetInfo()`: Obtiene `/api/dataset-info`, renderiza info grid y 3 gráficos
  - `chart-lugar`: Doughnut
  - `chart-estado`: Pie
  - `chart-defects-week`: Line

---

### 7. **js/loaders-analysis.js** (Análisis)
Carga gráficos de análisis:

- `loadKPICharts()`: Tendencia semanal, defectos top, calidad
  - `chart-weekly`: Line (tallos, proyección, exportación)
  - `chart-defects`: Horizontal bar
  - `chart-quality-prov`: Horizontal bar
  
- `loadSuppliers()`: Top proveedores y desviación
  - `chart-top-suppliers`: Bar
  - `chart-deviation`: Grouped bar
  
- `loadQuality()`: Defectos y calidad
  - `chart-defects2`: Bar
  - `chart-defects-week2`: Line
  - `chart-quality2`: Horizontal bar

---

### 8. **js/loaders-ml.js** (Machine Learning)
Carga de modelos ML:

- `loadML(name)`: Router que llama a la función específica
  
- `loadMLCompliance()`: Random Forest
  - `chart-rf-importance`: Horizontal bar
  - `chart-rf-scatter`: Scatter plot
  
- `loadMLCluster()`: K-Means
  - Renderiza cards de clusters
  - `chart-cluster-scatter`: Scatter plot coloreado
  
- `loadMLAnomaly()`: Isolation Forest
  - `chart-anomaly-prov`: Horizontal bar
  - `chart-anomaly-scatter`: Scatter plot (normal vs anómalo)
  
- `loadMLForecast()`: Regresión Lineal
  - `chart-forecast`: Line con historical + fitted + forecast

---

### 9. **js/main.js** (Inicialización)
Punto de entrada:

- `loadPage(name)`: Router de carga por tipo de página
  - Problemática: estática
  - Dataset: llama `loadDatasetInfo()`
  - KPIs: llama `loadKPICharts()`
  - Suppliers: llama `loadSuppliers()`
  - Quality: llama `loadQuality()`
  - ML: llama `loadML('compliance')`

- `init()`: IIFE que se ejecuta al cargar
  - Carga KPIs inmediatamente
  - Inicializa la página "problemática"

---

## Flujo de Ejecución

### 1. Al cargar la página
```
index.html carga
  ↓
utils.js (PALETTE, get, fmt)
  ↓
charts.js (mkChart)
  ↓
ui.js (showPage, showMLPanel)
  ↓
loaders-kpis.js
  ↓
loaders-analysis.js
  ↓
loaders-ml.js
  ↓
main.js → init() → loadKPIs()
```

### 2. Al hacer click en navegación
```
<a onclick="showPage('kpis')">
  ↓
showPage('kpis') en ui.js
  ↓
loadPage('kpis') en main.js
  ↓
loadKPICharts() en loaders-analysis.js
  ↓
mkChart('chart-weekly', ...) en charts.js
  ↓
fetch('/api/charts/weekly-trend')
```

---

## Ventajas de esta Estructura

| Aspecto | Antes | Después |
|--------|--------|---------|
| **Líneas en index.html** | 900 | 200 |
| **CSS inline** | Sí (400 líneas) | No (archivo separado) |
| **JS inline** | Sí (500 líneas) | No (7 archivos) |
| **Claridad de código** | Difícil navegar | Cada archivo tiene propósito claro |
| **Reutilización de funciones** | Acoplado | Funciones independientes |
| **Cacheo del navegador** | Monolítico | CSS y JS cacheados separately |
| **Testing** | Imposible aislar | Funciones testeables |

---

## Cómo Agregar Nuevas Funcionalidades

### Agregar un nuevo gráfico

1. **En `loaders-analysis.js`** (o nuevo archivo `loaders-*.js`):
```javascript
async function loadNewChart() {
  const data = await get('/api/charts/new-data');
  mkChart('chart-new', 'type', {
    labels: data.labels,
    datasets: [{ label: '...', data: data.values }]
  });
}
```

2. **En `index.html`** (agregar canvas):
```html
<div class="chart-card">
  <h3>Mi gráfico nuevo</h3>
  <div class="chart-wrap"><canvas id="chart-new"></canvas></div>
</div>
```

3. **En `main.js`** (agregar a loadPage):
```javascript
if (name === 'newpage') loadNewChart();
```

---

## Cómo Modificar Estilos

**Cambiar colores:**
```css
/* En styles.css */
:root {
  --accent: #6366f1;  /* Cambiar aquí */
}
```

**Agregar nuevo componente:**
```css
/* En styles.css al final */
.new-component {
  background: var(--surface);
  border: 1px solid var(--border);
  /* ... */
}
```

---

## Dependencias

- **Chart.js 4.4.1**: CDN (no incluida en archivos)
- **ES6+**: Async/await, spread operator, arrow functions
- **Fetch API**: Para solicitudes HTTP
- **CSS Grid & Flexbox**: Diseño responsive

---

## Próximos Pasos (Opcional)

- Agregar bundler (Webpack, Vite) para minificar
- Agregar unit tests para loaders
- Agregar service worker para offline
- Agregar TypeScript para mayor seguridad de tipos
- Separar componentes en Web Components
