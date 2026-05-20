"""Módulo de carga y limpieza de datos."""

import pandas as pd
import numpy as np
from scripts.config import FILE_PATH, DEFECT_COLS, NUMERIC_COLS, TEXT_COLS


def load_and_clean():
    """
    Carga el archivo Excel, limpia y prepara los datos.
    
    Returns:
        pd.DataFrame: DataFrame limpio y procesado
    """
    # Carga datos crudos
    raw = pd.read_excel(FILE_PATH, sheet_name="BASE GENERAL", header=None)
    
    # Extrae headers de la fila 3
    headers = raw.iloc[3].tolist()
    df = raw.iloc[4:].copy()
    df.columns = range(len(headers))
    
    # Renombra columnas basado en headers originales
    col_map = {i: h for i, h in enumerate(headers) if str(h) != "nan"}
    df = df.rename(columns=col_map)
    
    # Selecciona columnas a mantener (1-71 del original)
    keep = [headers[i] for i in range(1, 71) if str(headers[i]) != "nan"]
    df = df[[c for c in keep if c in df.columns]].copy()
    df.columns = df.columns.str.strip()
    
    # Elimina filas completamente vacías
    df.dropna(how="all", inplace=True)
    
    # Conversiones de tipo
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    
    for col in NUMERIC_COLS + DEFECT_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Limpieza de texto
    for col in TEXT_COLS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    # Elimina filas sin proveedor o tallos recibidos
    df = df[df["NOMBRE PROVEEDOR"].notna() & (df["NOMBRE PROVEEDOR"] != "nan")]
    df = df[df["TALLOS RECIBIDOS"].notna()]
    
    # Completa defectos con 0
    for col in DEFECT_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Columnas derivadas
    df["TOTAL_DEFECTOS"] = df[[c for c in DEFECT_COLS if c in df.columns]].sum(axis=1)
    df["MES"] = df["FECHA"].dt.month
    df["SEMANA"] = df["SEM"].fillna(0).astype(int)
    df["ES_EXPORTACION"] = (df["Exportación"].fillna(0) > 0).astype(int)
    
    # Índice de calidad: 0-100
    total_stems = df["TALLOS RECIBIDOS"].replace(0, np.nan)
    df["INDICE_CALIDAD"] = (1 - (df["TOTAL_DEFECTOS"] / total_stems).clip(0, 1)) * 100
    
    # Tasa de cumplimiento
    proj = df["PROYECCIÓN"].replace(0, np.nan)
    df["CUMPLIMIENTO"] = (df["TALLOS RECIBIDOS"] / proj).clip(0, 3) * 100
    
    df.reset_index(drop=True, inplace=True)
    return df
