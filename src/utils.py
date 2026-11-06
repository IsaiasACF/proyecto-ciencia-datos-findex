"""Tablas y gráficos descriptivos de inclusión financiera; sin métricas de modelos."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COUNTRY_LABELS = {
    "ARG": "Argentina", "BOL": "Bolivia", "BRA": "Brasil", "CHL": "Chile",
    "COL": "Colombia", "CRI": "Costa Rica", "DOM": "República Dominicana",
    "ECU": "Ecuador", "SLV": "El Salvador", "GTM": "Guatemala", "HTI": "Haití",
    "HND": "Honduras", "MEX": "México", "NIC": "Nicaragua", "PAN": "Panamá",
    "PRY": "Paraguay", "PER": "Perú", "TTO": "Trinidad y Tobago", "URY": "Uruguay",
    "VEN": "Venezuela",
}


def account_by_group(data, group, weights):
    """Proporción con cuenta por grupo, con n muestral y porcentaje ponderado.

    weights debe compartir exactamente el índice con data. Cada denominador
    usa únicamente personas con grupo y objetivo observados. No calcula IC.
    """
    if not data.index.equals(weights.index):
        raise ValueError("Los pesos y los datos deben tener el mismo índice y orden.")
    if not data["account_fin"].dropna().isin([0, 1]).all():
        raise ValueError("El objetivo debe estar codificado como 0/1.")
    if not (np.isfinite(weights) & weights.gt(0)).all():
        raise ValueError("Los pesos deben ser finitos y positivos.")
    work = data[[group, "account_fin"]].copy()
    work["peso"] = weights
    work = work.dropna(subset=[group, "account_fin"])
    work["peso_con_cuenta"] = work["peso"] * work["account_fin"]
    table = work.groupby(group, observed=True).agg(
        n=("account_fin", "size"), con_cuenta=("account_fin", "sum"),
        suma_pesos=("peso", "sum"), suma_pesos_con_cuenta=("peso_con_cuenta", "sum"),
    ).reset_index()
    table["sin_cuenta"] = table["n"] - table["con_cuenta"]
    table["porcentaje_con_cuenta_no_ponderado"] = 100 * table["con_cuenta"] / table["n"]
    table["porcentaje_con_cuenta_ponderado"] = 100 * table["suma_pesos_con_cuenta"] / table["suma_pesos"]
    return table


def plot_account_rates(table, label_column, title, destination, weighting, horizontal=False):
    """Guardar y mostrar proporciones con etiquetas de ponderación y universo."""
    values = table["porcentaje_con_cuenta_ponderado"]
    labels = table[label_column].astype(str)
    fig, ax = plt.subplots(figsize=(10, 8) if horizontal else (9, 5))
    if horizontal:
        ax.barh(labels, values, color="#34759b")
        ax.set_xlim(0, 105)
        ax.set_xlabel("Personas con cuenta (%)")
        for i, value in enumerate(values):
            ax.text(value + 0.6, i, f"{value:.1f}%", va="center", fontsize=9)
    else:
        ax.bar(labels, values, color="#34759b")
        ax.set_ylim(0, 105)
        ax.set_ylabel("Personas con cuenta (%)")
        for i, value in enumerate(values):
            ax.text(i, value + 1, f"{value:.1f}%", ha="center", fontsize=10)
        ax.tick_params(axis="x", labelsize=9)
    ax.set_title(title + "\n" + weighting + " · Casos completos", fontsize=12)
    fig.text(0.5, 0.015, "Fuente: Global Findex 2017. Asociaciones descriptivas; sin ajuste por otras variables.",
             ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(destination, dpi=150, bbox_inches="tight", metadata={"Software": "matplotlib"})
    plt.show()
    plt.close(fig)
