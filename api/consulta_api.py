"""Consulta a la API de Datos Abiertos (Socrata) del conjunto
'Casos positivos de COVID-19 en Colombia' (id: gt2j-8ykr).

Este módulo solo se encarga de OBTENER y FILTRAR los datos.
No imprime nada ni pide datos al usuario (eso es tarea del módulo ui).
"""
import pandas as pd
from sodapy import Socrata

DOMINIO = "www.datos.gov.co"
ID_DATASET = "gt2j-8ykr"
TIMEOUT_SEGUNDOS = 60

# Nombre que se muestra al usuario -> posibles columnas reales del dataset.
# Se listan varias porque el portal ha cambiado el esquema con el tiempo.
COLUMNAS_SALIDA = {
    "Ciudad de ubicación": ["ciudad_municipio_nom", "ciudad_de_ubicaci_n"],
    "Departamento": ["departamento_nom", "departamento"],
    "Edad": ["edad"],
    "Tipo": ["fuente_tipo_contagio", "tipo"],
    "Estado": ["estado"],
    "País de procedencia": ["pais_viajo_1_nom", "pais_de_procedencia"],
}

# Columnas por las que se puede filtrar el departamento (se prueban en orden).
COLUMNAS_FILTRO_DEPARTAMENTO = ["departamento_nom", "departamento"]


def _crear_cliente():
    """Cliente sin autenticación (el dataset es público)."""
    return Socrata(DOMINIO, None, timeout=TIMEOUT_SEGUNDOS)


def _primera_columna_existente(df, candidatas):
    for nombre in candidatas:
        if nombre in df.columns:
            return nombre
    return None


def _formatear(df):
    """Deja solo las columnas requeridas, con sus nombres legibles."""
    salida = pd.DataFrame()
    for titulo, candidatas in COLUMNAS_SALIDA.items():
        col = _primera_columna_existente(df, candidatas)
        salida[titulo] = df[col] if col else "N/D"
    return salida.fillna("N/D")


def consultar_casos(nombre_departamento, limite_registros):
    """Devuelve un DataFrame con los casos del departamento indicado.

    Parámetros:
        nombre_departamento (str): p. ej. "Risaralda".
        limite_registros (int): cantidad máxima de registros a traer.
    """
    client = _crear_cliente()
    variantes = [nombre_departamento.strip().upper(), nombre_departamento.strip()]

    ultimo_error = None
    for columna in COLUMNAS_FILTRO_DEPARTAMENTO:
        for valor in variantes:
            try:
                # Equivale a: client.get("gt2j-8ykr", limit=..., departamento=...)
                results = client.get(
                    ID_DATASET, limit=limite_registros, **{columna: valor}
                )
            except Exception as error:  # columna inexistente, red, timeout...
                ultimo_error = error
                continue
            if results:
                df = pd.DataFrame.from_records(results)
                return _formatear(df)

    if ultimo_error is not None:
        raise ConnectionError(f"No se pudo consultar la API: {ultimo_error}")
    return pd.DataFrame(columns=list(COLUMNAS_SALIDA))
