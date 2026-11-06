"""Carga, selección regional y limpieza de Global Findex 2017 (sin modelamiento)."""

from pathlib import Path

import numpy as np
import pandas as pd

MODEL_COLUMNS = ["account_fin", "age", "female", "educ", "inc_q", "emp_in", "mobileowner"]
AUX_COLUMNS = ["economy", "economycode", "regionwb", "wgt"]
SELECTED_COLUMNS = MODEL_COLUMNS + AUX_COLUMNS
LAC_REGION = "Latin America & Caribbean (excluding high income)"
# regionwb separa estas economías geográficamente caribeñas/latinoamericanas por ingreso.
LAC_HIGH_INCOME = {"CHL": "Chile", "TTO": "Trinidad and Tobago", "URY": "Uruguay"}
EXPECTED_LAC_CODES = {
    "ARG", "BOL", "BRA", "CHL", "COL", "CRI", "DOM", "ECU", "SLV", "GTM",
    "HTI", "HND", "MEX", "NIC", "PAN", "PRY", "PER", "TTO", "URY", "VEN",
}
VALID_CODES = {
    "account_fin": {0, 1}, "female": {1, 2}, "educ": {1, 2, 3},
    "inc_q": {1, 2, 3, 4, 5}, "emp_in": {0, 1}, "mobileowner": {1, 2},
}
# Verificados contra micro_world.sps y los metadatos oficiales del CSV.
MISSING_CODES = {"educ": {4, 5}, "mobileowner": {3, 4}}
LABELS = {
    "account_fin": {0: "No tiene cuenta", 1: "Tiene cuenta"},
    "female": {1: "Hombre", 2: "Mujer"},
    "educ": {1: "Primaria o menos", 2: "Secundaria", 3: "Terciaria o más"},
    "inc_q": {i: f"Quintil {i}" for i in range(1, 6)},
    "emp_in": {0: "Fuera de fuerza laboral", 1: "En fuerza laboral"},
    "mobileowner": {1: "Tiene teléfono", 2: "No tiene teléfono"},
}
MEANINGS = {
    "account_fin": "Tenencia de cuenta en una institución financiera",
    "age": "Edad en años (99 representa 99 o más)",
    "female": "Sexo de la persona encuestada",
    "educ": "Nivel educacional",
    "inc_q": "Quintil de ingreso del hogar dentro de su economía",
    "emp_in": "Participación en la fuerza laboral",
    "mobileowner": "Tenencia de teléfono móvil",
    "economy": "Nombre de la economía",
    "economycode": "Código de la economía",
    "regionwb": "Agrupación regional/de ingreso original del Banco Mundial",
    "wgt": "Peso muestral dentro de cada economía",
}


def load_findex(path):
    """Leer el CSV original sin modificarlo y comprobar las columnas requeridas."""
    data = pd.read_csv(Path(path))
    required = set(MODEL_COLUMNS + ["economy", "economycode", "regionwb"])
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")
    return data


def filter_lac(data):
    """Seleccionar LAC geográfica, auditando la lista de economías de esta versión."""
    selected = data["regionwb"].eq(LAC_REGION) | data["economycode"].isin(LAC_HIGH_INCOME)
    result = data.loc[selected].copy()
    found = set(result["economycode"].unique())
    if found != EXPECTED_LAC_CODES:
        raise ValueError(f"Cambió la cobertura; revisar economías: {sorted(found ^ EXPECTED_LAC_CODES)}")
    for code, name in LAC_HIGH_INCOME.items():
        names = set(result.loc[result["economycode"].eq(code), "economy"])
        if names != {name}:
            raise ValueError(f"Revisar correspondencia geográfica de {code}: {names}")
    return result


def clean_missing_values(data):
    """Recodificar solo no respuestas documentadas; rechazar códigos inesperados."""
    result = data.copy()
    for column in MODEL_COLUMNS:
        result[column] = pd.to_numeric(result[column], errors="raise")
    for column, codes in MISSING_CODES.items():
        result[column] = result[column].mask(result[column].isin(codes))
    for column, valid in VALID_CODES.items():
        unknown = set(result[column].dropna().unique()).difference(valid)
        if unknown:
            raise ValueError(f"Códigos no documentados en {column}: {sorted(unknown)}")
    ages = result["age"].dropna()
    if not (ages.between(15, 99) & ages.eq(ages.round())).all():
        raise ValueError("Edad fuera del dominio documentado 15–99 (99+); revisar fuente.")
    return result


def prepare_model_dataset(data):
    """Conservar casos completos en objetivo/predictores y solo columnas solicitadas.

    No exigir auxiliares completos, imputar, escalar, dividir ni entrenar modelos.
    Se conserva el índice de origen para alinear los pesos descriptivos en memoria.
    """
    columns = [column for column in SELECTED_COLUMNS if column in data]
    result = clean_missing_values(data[columns]).dropna(subset=MODEL_COLUMNS).copy()
    for column in MODEL_COLUMNS:
        result[column] = result[column].astype("int64")
    return result


def data_quality_summary(data, stage):
    """Resumir faltantes originales y no respuestas antes de eliminar filas."""
    recoded = clean_missing_values(data)
    rows = []
    for column in [c for c in SELECTED_COLUMNS if c in data]:
        missing_raw = int(data[column].isna().sum())
        missing = int(recoded[column].isna().sum())
        if column in LABELS:
            possible = "; ".join(f"{k}: {v}" for k, v in LABELS[column].items())
        elif column == "age":
            possible = "15–98 años; 99 = 99 o más"
        elif column == "wgt":
            possible = "Número real positivo"
        else:
            possible = "; ".join(sorted(data[column].dropna().unique()))
        rows.append({
            "etapa": stage, "variable": column, "significado": MEANINGS[column],
            "tipo": str(data[column].dtype), "valores_validos": possible,
            "n_total": len(data), "n_validos": len(data) - missing,
            "faltantes_originales": missing_raw,
            "no_respuesta_recodificada": missing - missing_raw,
            "faltantes_total": missing, "faltantes_pct": 100 * missing / len(data),
        })
    return pd.DataFrame(rows)


def regional_weight_reference(lac):
    """Calcular factores poblacionales por economía ANTES de eliminar casos.

    pop_adult proviene del CSV: población 15+, 2016, WDI.
    El factor convierte wgt, normalizado por país, a peso de población adulta.
    Es auxiliar descriptivo: no se agrega al dataset de modelamiento.
    """
    for column in ["wgt", "pop_adult"]:
        if column not in lac or not (np.isfinite(lac[column]) & lac[column].gt(0)).all():
            raise ValueError(f"{column} ausente o inválido: no calcular ponderación regional.")
    if not lac.groupby("economycode")["pop_adult"].nunique().eq(1).all():
        raise ValueError("Población adulta inconsistente dentro de una economía.")
    reference = lac.groupby(["economy", "economycode"], as_index=False).agg(
        n_original=("wgt", "size"), suma_wgt_original=("wgt", "sum"),
        media_wgt=("wgt", "mean"), min_wgt=("wgt", "min"), max_wgt=("wgt", "max"),
        poblacion_15_mas_2016=("pop_adult", "first"),
    )
    reference["factor_poblacion"] = reference["poblacion_15_mas_2016"] / reference["suma_wgt_original"]
    return reference


def regional_weights(data, reference):
    """Alinear pesos poblacionales con el índice sin renormalizar tras la limpieza."""
    factors = reference.set_index("economycode")["factor_poblacion"]
    weights = data["wgt"] * data["economycode"].map(factors)
    if not (np.isfinite(weights) & weights.gt(0)).all():
        raise ValueError("Pesos regionales inválidos o referencia incompleta.")
    return weights
