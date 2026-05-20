"""Módulo para generación de datos de gráficos."""

import numpy as np
from scripts.config import DEFECT_COLS
from scripts.kpis import safe_float


def top_suppliers_volume(df, n=10):
    """Top N proveedores por volumen de tallos."""
    grp = df.groupby("NOMBRE PROVEEDOR")["TALLOS RECIBIDOS"].sum().nlargest(n)
    return {"labels": grp.index.tolist(), "values": grp.values.tolist()}


def top_defects(df):
    """Ranking de defectos más comunes."""
    totals = {c: int(df[c].sum()) for c in DEFECT_COLS if c in df.columns}
    sorted_d = dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))
    return {"labels": list(sorted_d.keys()), "values": list(sorted_d.values())}


def supplier_deviation(df, n=10):
    """Proveedores con mayor desviación en cumplimiento."""
    grp = df.groupby("NOMBRE PROVEEDOR")["CUMPLIMIENTO"].agg(["mean", "std"]).dropna()
    grp.columns = ["media", "desviacion"]
    top = grp.nlargest(n, "desviacion")
    return {
        "labels": top.index.tolist(),
        "media": [safe_float(v) for v in top["media"]],
        "desviacion": [safe_float(v) for v in top["desviacion"]],
    }


def weekly_trend(df):
    """Tendencia semanal: tallos, exportación y proyección."""
    grp = df.groupby("SEMANA").agg(
        tallos=("TALLOS RECIBIDOS", "sum"),
        exportacion=("Exportación", "sum"),
        proyeccion=("PROYECCIÓN", "sum"),
    ).reset_index().sort_values("SEMANA")
    return {
        "semanas": grp["SEMANA"].tolist(),
        "tallos": grp["tallos"].fillna(0).tolist(),
        "exportacion": grp["exportacion"].fillna(0).tolist(),
        "proyeccion": grp["proyeccion"].fillna(0).tolist(),
    }


def quality_by_supplier(df, n=10):
    """Proveedores con mejor índice de calidad."""
    grp = (df[df["TALLOS RECIBIDOS"] > 50]
           .groupby("NOMBRE PROVEEDOR")["INDICE_CALIDAD"]
           .mean()
           .nlargest(n))
    return {"labels": grp.index.tolist(), "values": [safe_float(v) for v in grp.values]}


def lugar_distribution(df):
    """Distribución de tallos por lugar."""
    grp = df.groupby("LUGAR")["TALLOS RECIBIDOS"].sum().sort_values(ascending=False)
    return {"labels": grp.index.tolist(), "values": grp.values.tolist()}


def estado_distribution(df):
    """Distribución de registros por estado."""
    grp = df["ESTADO"].value_counts().head(6)
    return {"labels": grp.index.tolist(), "values": grp.values.tolist()}


def defects_over_weeks(df):
    """Tasa de defectos por semana."""
    d = df.copy()
    grp = d.groupby("SEMANA").agg(
        defectos=("TOTAL_DEFECTOS", "sum"),
        tallos=("TALLOS RECIBIDOS", "sum")
    ).reset_index()
    grp["tasa"] = (grp["defectos"] / grp["tallos"].replace(0, np.nan) * 100).fillna(0)
    return {
        "semanas": grp["SEMANA"].tolist(),
        "tasa": [safe_float(v) for v in grp["tasa"]],
    }
