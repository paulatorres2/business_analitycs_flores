"""
Aplicación Flask para análisis de datos de flores.
Punto de entrada principal - importa lógica de módulos especializados.
"""

import warnings
warnings.filterwarnings("ignore")

from flask import Flask, jsonify, render_template

from scripts.data_loader import load_and_clean
from scripts.kpis import calculate_kpis, get_dataset_info
from scripts.charts import (
    top_suppliers_volume, top_defects, supplier_deviation, weekly_trend,
    quality_by_supplier, lugar_distribution, estado_distribution, defects_over_weeks
)
from scripts.ml_models import predict_compliance, cluster_suppliers, anomaly_detection, forecast_stems

app = Flask(__name__)

# ─────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────
print("Loading and cleaning data…")
DF = load_and_clean()
print(f"Dataset ready: {DF.shape[0]:,} rows × {DF.shape[1]} cols")

# ─────────────────────────────────────────────
# RUTAS - INICIO
# ─────────────────────────────────────────────
@app.route("/")
def index():
    """Página principal."""
    return render_template("index.html")

# ─────────────────────────────────────────────
# RUTAS - KPIs Y DATASET
# ─────────────────────────────────────────────
@app.route("/api/kpis")
def api_kpis():
    """Retorna KPIs principales."""
    return jsonify(calculate_kpis(DF))

@app.route("/api/dataset-info")
def api_dataset_info():
    """Retorna información del dataset."""
    return jsonify(get_dataset_info(DF))

# ─────────────────────────────────────────────
# RUTAS - GRÁFICOS
# ─────────────────────────────────────────────
@app.route("/api/charts/top-suppliers")
def api_top_suppliers():
    """Top 10 proveedores por volumen."""
    return jsonify(top_suppliers_volume(DF))

@app.route("/api/charts/top-defects")
def api_top_defects():
    """Ranking de defectos."""
    return jsonify(top_defects(DF))

@app.route("/api/charts/supplier-deviation")
def api_supplier_deviation():
    """Proveedores con mayor desviación."""
    return jsonify(supplier_deviation(DF))

@app.route("/api/charts/weekly-trend")
def api_weekly_trend():
    """Tendencia semanal."""
    return jsonify(weekly_trend(DF))

@app.route("/api/charts/quality-by-supplier")
def api_quality_supplier():
    """Calidad por proveedor."""
    return jsonify(quality_by_supplier(DF))

@app.route("/api/charts/lugar-distribution")
def api_lugar():
    """Distribución por lugar."""
    return jsonify(lugar_distribution(DF))

@app.route("/api/charts/estado-distribution")
def api_estado():
    """Distribución por estado."""
    return jsonify(estado_distribution(DF))

@app.route("/api/charts/defects-over-weeks")
def api_defects_weeks():
    """Defectos por semana."""
    return jsonify(defects_over_weeks(DF))

# ─────────────────────────────────────────────
# RUTAS - MODELOS ML
# ─────────────────────────────────────────────
@app.route("/api/ml/compliance")
def api_ml_compliance():
    """Predicción de cumplimiento (Random Forest)."""
    return jsonify(predict_compliance(DF))

@app.route("/api/ml/clusters")
def api_ml_clusters():
    """Clustering de proveedores (K-Means)."""
    return jsonify(cluster_suppliers(DF))

@app.route("/api/ml/anomaly")
def api_ml_anomaly():
    """Detección de anomalías (Isolation Forest)."""
    return jsonify(anomaly_detection(DF))

@app.route("/api/ml/forecast")
def api_ml_forecast():
    """Pronóstico de tallos (Regresión Lineal)."""
    return jsonify(forecast_stems(DF))

# ─────────────────────────────────────────────
# INICIO
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)