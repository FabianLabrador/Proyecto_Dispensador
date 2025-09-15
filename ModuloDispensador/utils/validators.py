# /utils/validators.py

from data_access.config import COLUMNAS_REQUERIDAS

def validar_datos(df):
    errores = []

    for col in COLUMNAS_REQUERIDAS:
        if col not in df.columns:
            errores.append(f"Falta la columna obligatoria: {col}")

    if df.empty:
        errores.append("El archivo está vacío")

    return errores
