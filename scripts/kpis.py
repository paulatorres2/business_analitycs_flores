"""Módulo de cálculos de KPIs."""

import numpy as np
import pandas as pd


def safe_float(v):
    """Convierte valor a float seguro, retorna 0 si es NaN."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return 0.0
    return round(float(v), 2)


def calculate_kpis(df):
    """
    Calcula KPIs principales del dataset.
    
    Args:
        df (pd.DataFrame): DataFrame con datos limpios
        
    Returns:
        dict: Diccionario con todos los KPIs
    """
    total_stems = df["TALLOS RECIBIDOS"].sum()
    total_export = df["Exportación"].fillna(0).sum()
    total_defects = df["TOTAL_DEFECTOS"].sum()
    
    cum_prom = safe_float(df["CUMPLIMIENTO"].median())
    tasa_exp = safe_float(total_export / total_stems * 100) if total_stems else 0
    tasa_rec_nal = safe_float(df["Total Nacional"].fillna(0).sum() / total_stems * 100) if total_stems else 0
    idx_calidad = safe_float(df["INDICE_CALIDAD"].mean())
    
    return {
        "cumplimiento_prom": cum_prom,
        "tasa_exportacion": tasa_exp,
        "tasa_rechazo_nacional": tasa_rec_nal,
        "indice_calidad": idx_calidad,
        "total_tallos": int(total_stems),
        "total_proveedores": int(df["NOMBRE PROVEEDOR"].nunique()),
        "total_registros": len(df),
        "semanas": int(df["SEMANA"].nunique()),
    }


def get_dataset_info(df):
    """
    Obtiene información general del dataset.
    
    Args:
        df (pd.DataFrame): DataFrame con datos limpios
        
    Returns:
        dict: Información del dataset
    """
    missing = {c: int(df[c].isna().sum()) for c in df.columns if df[c].isna().sum() > 0}
    top_missing = dict(sorted(missing.items(), key=lambda x: x[1], reverse=True)[:8])
    fecha_min = df["FECHA"].min()
    fecha_max = df["FECHA"].max()
    
    return {
        "filas_originales": 14911,
        "filas_limpias": len(df),
        "columnas": len(df.columns),
        "fecha_inicio": str(fecha_min.date()) if pd.notna(fecha_min) else "N/A",
        "fecha_fin": str(fecha_max.date()) if pd.notna(fecha_max) else "N/A",
        "proveedores_unicos": int(df["NOMBRE PROVEEDOR"].nunique()),
        "variedades_unicas": int(df["VARIEDAD"].nunique()),
        "lugares_destino": int(df["LUGAR"].nunique()),
        "semanas_cubiertas": int(df["SEMANA"].nunique()),
        "pct_nulos": round(df.isnull().mean().mean() * 100, 1),
        "top_missing": top_missing,
        "columnas_categoricas": int(df.select_dtypes("object").shape[1]),
        "columnas_numericas": int(df.select_dtypes(np.number).shape[1]),
    }
