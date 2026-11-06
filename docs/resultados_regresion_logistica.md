# Resultados de la regresión logística — Grupo 10

## Datos y especificación

Base validada de Global Findex 2017: 18,927 personas de 20 economías de América Latina y el Caribe. Se usan únicamente edad, sexo, educación, quintil de ingreso, participación laboral y teléfono móvil. Pipeline original: edad centrada con la media de entrenamiento y One-Hot con referencia para las cinco variables categóricas; regresión logística L2, C=1, solver lbfgs. No se incluyen país, pesos muestrales ni otros modelos. Objetivo: 0 = sin cuenta; 1 = con cuenta.

## Desempeño holdout

Partición estratificada 80/20, semilla 42: 15,141 personas en entrenamiento y 3,786 en prueba. Con el umbral original de 0,5, accuracy = **0,6416**, ROC-AUC = **0,6981** y F1 macro = **0,6414**. El baseline mayoritario tiene accuracy 0,5013; la mejora es de 14,03 puntos porcentuales.

| Clase | Precision | Recall | F1 | Personas reales |
|---|---:|---:|---:|---:|
| Sin cuenta | 0,6458 | 0,6229 | 0,6341 | 1888 |
| Con cuenta | 0,6377 | 0,6602 | 0,6487 | 1898 |

## Sensibilidad y especificidad para personas sin cuenta

Considerando **sin cuenta como clase positiva**, sensibilidad = **62,29%** (1176/1888): proporción de personas sin cuenta detectadas. Especificidad = **66,02%** (1253/1898): proporción de personas con cuenta correctamente reconocidas como con cuenta. Se omiten 712 personas sin cuenta y se clasifican como sin cuenta 645 personas que sí tienen cuenta. Especificidad y precision son métricas distintas.

## Validación cruzada

Se mantienen los mismos cinco folds estratificados dentro del entrenamiento, con shuffle=True y semilla 42. Cada fold reajusta una copia de la pipeline original sin usar el test. La desviación estándar es muestral (ddof=1), no un intervalo de confianza. F1 se calcula por clase y su promedio macro no pondera por frecuencia.

| Métrica | Media ± desviación estándar | Test actual |
|---|---:|---:|
| Accuracy | 0,6458 ± 0,0037 | 0,6416 |
| F1 sin cuenta | 0,6427 ± 0,0050 | 0,6341 |
| F1 con cuenta | 0,6488 ± 0,0050 | 0,6487 |
| F1 macro | 0,6457 ± 0,0037 | 0,6414 |
| ROC-AUC | 0,7026 ± 0,0060 | 0,6981 |

La dispersión entre folds es pequeña y los promedios son cercanos al test. El modelo parece estable ante estas particiones, con capacidad predictiva limitada; estabilidad no equivale a rendimiento alto.

## Odds ratios y asociaciones ajustadas

Los siguientes OR comparan las odds de **tener cuenta**, manteniendo constantes las demás variables. No representan cambios de probabilidad ni efectos causales. Las referencias son hombre, primaria o menos, quintil 1, fuera de fuerza laboral y sin teléfono. El OR de edad corresponde a un año adicional.

| Característica | Referencia | Odds ratio |
|---|---|---:|
| Edad: un año adicional | Edad centrada en media de entrenamiento | 1,019 |
| Mujer | Hombre | 0,942 |
| Secundaria | Primaria o menos | 1,803 |
| Terciaria o más | Primaria o menos | 4,238 |
| Quintil 2 | Quintil 1 | 1,252 |
| Quintil 3 | Quintil 1 | 1,475 |
| Quintil 4 | Quintil 1 | 1,692 |
| Quintil 5 | Quintil 1 | 2,330 |
| En fuerza laboral | Fuera de fuerza laboral | 1,557 |
| Tiene teléfono | No tiene teléfono | 2,403 |

Entre las comparaciones categóricas destacan educación terciaria frente a primaria o menos, teléfono frente a ausencia de teléfono y quintil 5 frente a quintil 1, asociados con mayores odds ajustadas de tener cuenta. Educación e ingreso muestran OR crecientes respecto de sus referencias. Participar en la fuerza laboral también se asocia con mayores odds. La estimación de mujer frente a hombre es cercana a uno y ligeramente menor. La edad presenta una asociación positiva por año. No se utiliza la magnitud de los OR como jerarquía universal de importancia: las referencias y unidades son diferentes.

## Limitaciones

- Datos observacionales de 2017: **asociación no implica causalidad** y no se demuestra estabilidad temporal.
- País omitido y división aleatoria dentro de la mezcla regional: no se evalúa generalización a economías no vistas y puede persistir heterogeneidad geográfica.
- Entrenamiento y métricas sin ponderación muestral; los resultados describen la muestra, no estimaciones representativas de la población regional.
- Selección de casos completos y cobertura parcial del Caribe: posibles sesgos de selección.
- Edad lineal en log-odds y valor superior 99+ representado como 99; no se exploran relaciones más flexibles.
- Coeficientes regularizados L2, sin intervalos de confianza ni pruebas de significancia. El umbral no se optimizó. El test ya fue consultado y no debe convertirse en una fuente de ajustes repetidos.

Fuentes reproducibles: notebook 02; outputs/metrics/logistic_model_comparison.csv, logistic_metrics.csv, logistic_cross_validation.csv y logistic_sensitivity_specificity.csv; outputs/tables/logistic_coefficients.csv. Las métricas de este informe se derivan exclusivamente del modelo y de los folds actuales, sin cambios de hiperparámetros.
