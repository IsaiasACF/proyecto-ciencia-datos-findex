"""Evaluación reproducible de clasificadores binarios de tenencia de cuenta."""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score


def evaluate_binary_classifier(y_true, y_pred, probability_one, model_name):
    """Retornar métricas globales y por clase sin ponderación muestral.

    probability_one corresponde siempre a account_fin=1. Para la clase 0 se
    evalúa su indicador contra 1-probability_one. La precisión sin predicciones
    de una clase se registra como 0 (zero_division=0), incluido el baseline.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    probability_one = np.asarray(probability_one)
    if not (y_true.shape == y_pred.shape == probability_one.shape) or y_true.ndim != 1:
        raise ValueError("Objetivo, predicciones y probabilidades deben ser vectores alineados.")
    if set(np.unique(y_true)) != {0, 1} or not set(np.unique(y_pred)) <= {0, 1}:
        raise ValueError("Se requieren ambas clases 0/1 en el objetivo y predicciones binarias.")
    if not (np.isfinite(probability_one) & (probability_one >= 0) & (probability_one <= 1)).all():
        raise ValueError("Las probabilidades deben ser finitas y pertenecer a [0, 1].")
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1], zero_division=0,
    )
    per_class = pd.DataFrame({
        "modelo": model_name, "clase": [0, 1], "etiqueta": ["Sin cuenta", "Con cuenta"],
        "precision": precision, "recall": recall, "f1_score": f1, "n_real": support,
        "roc_auc_uno_contra_resto": [
            roc_auc_score(y_true == 0, 1 - probability_one),
            roc_auc_score(y_true == 1, probability_one),
        ],
    })
    overall = {
        "modelo": model_name, "n_prueba": len(y_true),
        "accuracy": accuracy_score(y_true, y_pred),
        "roc_auc_clase_1": roc_auc_score(y_true, probability_one),
        "f1_macro": float(np.mean(f1)),
    }
    return overall, per_class
