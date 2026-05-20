"""Configuración y constantes de la aplicación."""

import os

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = r"C:\Users\1003t\OneDrive\Escritorio\business_analitycs_flores\data\PROGRAMACIÓN Y CONTROL 2026.xlsx"

# Columnas de defectos
DEFECT_COLS = [
    "Araña", "Afidos", "Botritis", "M. Polvoso", "M. Velloso",
    "Trhips", "Maltrato", "Abierto", "C. Deforme", "C. Pequeña",
    "Deshidratacion", "Descabece", "T. Corto", "Trozador", "T. Debil",
    "Azulamiento", "Torcidos", "Follaje", "Punto De Corte", "Otros"
]

# Columnas numéricas para conversión
NUMERIC_COLS = [
    "SEM", "PROYECCIÓN", "TALLOS RECIBIDOS", "% CUMPLI",
    "Exportación", "Nacional", "Total flor P.", "Total Nacional"
]

# Columnas de texto para limpieza
TEXT_COLS = ["CODIGO PROV.", "NOMBRE PROVEEDOR", "LUGAR", "ESTADO"]
