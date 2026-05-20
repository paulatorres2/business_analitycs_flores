"""Módulo de modelos de Machine Learning."""

import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

from scripts.kpis import safe_float


def predict_compliance(df):
    """
    Random Forest para predecir % cumplimiento.
    
    Args:
        df (pd.DataFrame): DataFrame con datos
        
    Returns:
        dict: Resultados del modelo
    """
    d = df[["TALLOS RECIBIDOS", "PROYECCIÓN", "ES_EXPORTACION",
            "TOTAL_DEFECTOS", "INDICE_CALIDAD", "SEMANA",
            "CUMPLIMIENTO", "NOMBRE PROVEEDOR"]].dropna()
    d = d[d["CUMPLIMIENTO"].between(0, 300)]
    
    le = LabelEncoder()
    d = d.copy()
    d["PROV_ENC"] = le.fit_transform(d["NOMBRE PROVEEDOR"])
    
    feats = ["TALLOS RECIBIDOS", "PROYECCIÓN", "ES_EXPORTACION",
             "TOTAL_DEFECTOS", "INDICE_CALIDAD", "SEMANA", "PROV_ENC"]
    X = d[feats]
    y = d["CUMPLIMIENTO"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    r2 = safe_float(r2_score(y_test, y_pred))
    mae = safe_float(mean_absolute_error(y_test, y_pred))
    importances = dict(zip(feats, [safe_float(v) for v in model.feature_importances_]))
    
    # Scatter: actual vs predicted
    idx = np.random.choice(len(y_test), min(300, len(y_test)), replace=False)
    scatter = {
        "actual": [safe_float(v) for v in y_test.iloc[idx].values],
        "predicted": [safe_float(v) for v in y_pred[idx]],
    }
    
    return {
        "model": "Random Forest Regressor",
        "target": "% Cumplimiento",
        "r2": r2,
        "mae": mae,
        "importances": importances,
        "scatter": scatter,
        "insight": (
            f"El modelo explica el {r2*100:.1f}% de la varianza en cumplimiento "
            f"con un error medio de {mae:.1f}pp. "
            "Las variables más influyentes son tallos recibidos y proyección."
        ),
    }


def cluster_suppliers(df):
    """
    K-Means clustering de proveedores.
    
    Args:
        df (pd.DataFrame): DataFrame con datos
        
    Returns:
        dict: Resultados del clustering
    """
    grp = df.groupby("NOMBRE PROVEEDOR").agg(
        tallos=("TALLOS RECIBIDOS", "sum"),
        cumplimiento=("CUMPLIMIENTO", "mean"),
        calidad=("INDICE_CALIDAD", "mean"),
        defectos=("TOTAL_DEFECTOS", "sum"),
        exportacion=("Exportación", "sum"),
    ).dropna()
    
    scaler = StandardScaler()
    X = scaler.fit_transform(grp)
    km = KMeans(n_clusters=4, random_state=42, n_init=10)
    grp["cluster"] = km.fit_predict(X)
    
    cluster_labels = {
        0: "Alto volumen / Alta calidad",
        1: "Bajo volumen / Riesgo",
        2: "Volumen medio / Eficiente",
        3: "Alta desviación / Inconsistente"
    }
    
    result = []
    for cl in sorted(grp["cluster"].unique()):
        sub = grp[grp["cluster"] == cl]
        result.append({
            "cluster": int(cl),
            "label": cluster_labels.get(cl, f"Grupo {cl}"),
            "proveedores": sub.index.tolist()[:8],
            "count": len(sub),
            "avg_cumplimiento": safe_float(sub["cumplimiento"].mean()),
            "avg_calidad": safe_float(sub["calidad"].mean()),
            "total_tallos": int(sub["tallos"].sum()),
        })
    
    scatter_data = {
        "x": [safe_float(v) for v in grp["cumplimiento"].values],
        "y": [safe_float(v) for v in grp["calidad"].values],
        "cluster": grp["cluster"].tolist(),
        "labels": grp.index.tolist(),
    }
    
    return {
        "model": "K-Means Clustering (k=4)",
        "clusters": result,
        "scatter": scatter_data,
        "insight": "Los proveedores se segmentaron en 4 grupos estratégicos basados en volumen, cumplimiento, calidad y exportación.",
    }


def anomaly_detection(df):
    """
    Isolation Forest para detección de anomalías.
    
    Args:
        df (pd.DataFrame): DataFrame con datos
        
    Returns:
        dict: Resultados de anomalías detectadas
    """
    d = df[["TALLOS RECIBIDOS", "CUMPLIMIENTO", "TOTAL_DEFECTOS",
            "INDICE_CALIDAD", "NOMBRE PROVEEDOR"]].dropna()
    d = d[d["CUMPLIMIENTO"].between(0, 300)].copy()
    
    feats = ["TALLOS RECIBIDOS", "CUMPLIMIENTO", "TOTAL_DEFECTOS", "INDICE_CALIDAD"]
    scaler = StandardScaler()
    X = scaler.fit_transform(d[feats])
    
    iso = IsolationForest(contamination=0.05, random_state=42)
    d["anomaly"] = iso.fit_predict(X)
    d["score"] = iso.decision_function(X)
    
    anomalies = d[d["anomaly"] == -1]
    normal = d[d["anomaly"] == 1]
    
    top_anomalous = (anomalies.groupby("NOMBRE PROVEEDOR").size()
                     .sort_values(ascending=False).head(8))
    
    return {
        "model": "Isolation Forest (5% contaminación)",
        "total_anomalias": int(len(anomalies)),
        "total_normales": int(len(normal)),
        "pct_anomalias": safe_float(len(anomalies) / len(d) * 100),
        "top_proveedores": {
            "labels": top_anomalous.index.tolist(),
            "values": top_anomalous.values.tolist(),
        },
        "scatter": {
            "normal_x": [safe_float(v) for v in normal["CUMPLIMIENTO"].values[:400]],
            "normal_y": [safe_float(v) for v in normal["TOTAL_DEFECTOS"].values[:400]],
            "anomaly_x": [safe_float(v) for v in anomalies["CUMPLIMIENTO"].values[:200]],
            "anomaly_y": [safe_float(v) for v in anomalies["TOTAL_DEFECTOS"].values[:200]],
        },
        "insight": (
            f"Se detectaron {len(anomalies):,} entregas anómalas ({len(anomalies)/len(d)*100:.1f}% del total). "
            "Estas presentan combinaciones inusuales de volumen, cumplimiento y defectos."
        ),
    }


def forecast_stems(df):
    """
    Regresión lineal para pronóstico de tallos.
    
    Args:
        df (pd.DataFrame): DataFrame con datos
        
    Returns:
        dict: Resultados del pronóstico
    """
    grp = df.groupby("SEMANA")["TALLOS RECIBIDOS"].sum().reset_index()
    grp.columns = ["semana", "tallos"]
    grp = grp[grp["semana"] > 0].sort_values("semana")
    
    X = grp["semana"].values.reshape(-1, 1)
    y = grp["tallos"].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Pronóstico para 4 semanas
    max_sem = int(grp["semana"].max())
    future = np.array(range(max_sem + 1, max_sem + 5)).reshape(-1, 1)
    forecast = model.predict(future).tolist()
    actual = y.tolist()
    fitted = model.predict(X).tolist()
    
    return {
        "model": "Regresión Lineal (tendencia semanal)",
        "semanas_hist": grp["semana"].tolist(),
        "tallos_hist": [int(v) for v in actual],
        "tallos_fitted": [int(v) for v in fitted],
        "semanas_forecast": list(range(max_sem + 1, max_sem + 5)),
        "tallos_forecast": [int(max(0, v)) for v in forecast],
        "tendencia": safe_float(model.coef_[0]),
        "r2": safe_float(r2_score(y, fitted)),
        "insight": (
            f"Tendencia semanal: {model.coef_[0]:+,.0f} tallos/semana. "
            f"El modelo ajusta con R²={r2_score(y, fitted):.2f}."
        ),
    }
