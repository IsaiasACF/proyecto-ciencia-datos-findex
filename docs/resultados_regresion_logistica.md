# Resultados de la regresión logística — Grupo 10

## Datos y especificación

Base validada de Global Findex 2017: 18.927 personas de 20 economías de América Latina y el Caribe. Se usan únicamente edad, sexo, educación, quintil de ingreso, participación laboral y teléfono móvil. Pipeline original: edad centrada con la media de entrenamiento y One-Hot con referencia para las cinco variables categóricas; regresión logística L2, C=1, solver lbfgs. No se incluyen país, pesos muestrales ni otros modelos. Objetivo: 0 = sin cuenta; 1 = con cuenta.

## Desempeño holdout

Partición estratificada 80/20, semilla 42: 15.141 personas en entrenamiento y 3.786 en prueba. Con el umbral original de 0,5, accuracy = **64,16% (0,6416)**, ROC-AUC = **0,6981** y F1 macro = **0,6414**. El baseline mayoritario tiene accuracy 0,5013; la mejora es de 14,03 puntos porcentuales.

| Clase | Precision | Recall | F1 | Personas reales |
|---|---:|---:|---:|---:|
| Sin cuenta | 0,6458 | 0,6229 | 0,6341 | 1888 |
| Con cuenta | 0,6377 | 0,6602 | 0,6487 | 1898 |

## Sensibilidad y especificidad para personas sin cuenta

Considerando **sin cuenta como clase positiva**, sensibilidad = **62,29%** (1176/1888): proporción de personas sin cuenta detectadas. Especificidad = **66,02%** (1253/1898): proporción de personas con cuenta correctamente reconocidas como con cuenta. Se omiten **712 de 1.888 personas sin cuenta: 37,71% (aproximadamente 37,7%)**, y se clasifican como sin cuenta 645 personas que sí tienen cuenta. Especificidad y precision son métricas distintas.

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

Las asociaciones ajustadas de las seis variables se interpretan así, **manteniendo constantes las demás variables del modelo**:

- **Educación:** secundaria presenta OR 1,803 y terciaria o más OR 4,238, frente a primaria o menos. Se observan mayores odds de tener cuenta en los niveles educativos superiores.
- **Teléfono móvil:** poseer teléfono presenta OR 2,403 frente a no poseerlo, asociado con mayores odds de tener cuenta.
- **Quintil de ingreso:** los OR aumentan desde 1,252 en quintil 2 hasta 2,330 en quintil 5, respecto del quintil 1. Los quintiles son relativos al ingreso dentro de cada economía, no montos absolutos comparables entre países.
- **Participación laboral:** estar en la fuerza laboral presenta OR 1,557 frente a estar fuera. Participación laboral no equivale necesariamente a tener empleo.
- **Edad:** un año adicional presenta OR 1,019, una asociación positiva por año bajo el supuesto de linealidad en log-odds.
- **Sexo:** mujer frente a hombre presenta OR 0,942, una estimación ligeramente menor que uno y cercana a la ausencia de diferencia en odds. Sin intervalos de confianza no se afirma significancia estadística.

Educación, teléfono e ingreso muestran las mayores diferencias entre las comparaciones categóricas destacadas. Esto no constituye una jerarquía universal de importancia predictiva: los OR tienen referencias y unidades distintas y no son razones de probabilidades.

## Grupos con menor inclusión observados en el EDA

Los siguientes porcentajes con cuenta provienen de las tablas existentes de la Fase 1 y corresponden a casos completos. Son **asociaciones marginales ponderadas con wgt y población adulta**, sin ajuste por las demás características; no deben confundirse con los OR ajustados ni con las métricas de test, que son no ponderadas. Cada fila compara grupos por separado, no un perfil conjunto.

| Característica | Grupo con menor porcentaje con cuenta | Porcentaje | Comparación | Porcentaje |
|---|---|---:|---|---:|
| Ingreso | Quintil 1 | 38,96% | Quintil 5 | 73,78% |
| Educación | Primaria o menos | 43,82% | Terciaria o más | 77,55% |
| Teléfono | No tiene teléfono | 33,43% | Tiene teléfono | 59,97% |
| Participación laboral | Fuera de fuerza laboral | 43,50% | En fuerza laboral | 59,55% |
| Edad | 15–24 años | 38,55% | 25–34 años | 61,87% |
| Sexo | Mujer | 51,50% | Hombre | 57,72% |

El EDA muestra menor inclusión relativa entre personas de menores ingresos, menor educación, sin teléfono, fuera de la fuerza laboral, jóvenes de 15–24 años y mujeres frente a sus grupos de comparación. La edad no presenta un aumento continuo de la proporción con cuenta en todos los grupos etarios.

Por economía, ponderando **solo con wgt dentro de cada país**, las proporciones van de 28,07% en Haití a 80,84% en Trinidad y Tobago. Esta heterogeneidad no demuestra que el país explique más que las variables individuales y no está ajustada por la regresión.

## Limitaciones

- **Solo seis predictores:** pueden omitirse factores relevantes; la predicción es parcial y no caracteriza todas las barreras de inclusión financiera.
- **Detección incompleta:** se omite aproximadamente el **37,7% de las personas sin cuenta** del test (712 de 1.888), pese a la estabilidad entre folds.
- Datos observacionales de **2017**: no describen necesariamente la situación actual ni demuestran estabilidad temporal. **Asociación no implica causalidad**.
- País omitido y división aleatoria dentro de la mezcla regional: no se evalúa generalización a economías no vistas y puede persistir heterogeneidad geográfica.
- Entrenamiento y métricas sin ponderación muestral; los resultados describen la muestra, no estimaciones representativas de la población regional.
- Selección de casos completos y cobertura parcial del Caribe: posibles sesgos de selección.
- Edad lineal en log-odds y valor superior 99+ representado como 99; no se exploran relaciones más flexibles.
- Coeficientes regularizados L2, sin intervalos de confianza ni pruebas de significancia. El umbral no se optimizó. El test ya fue consultado y no debe convertirse en una fuente de ajustes repetidos.

## Conclusión

Las seis características consideradas —educación, teléfono móvil, quintil de ingreso, participación laboral, edad y sexo— permiten una predicción parcial de la tenencia de cuenta en los adultos de las economías estudiadas. Educación superior, poseer teléfono e ingresos más altos destacan en las comparaciones de odds ajustadas; la participación laboral y la edad también presentan asociaciones positivas, mientras que la diferencia estimada por sexo es pequeña. El modelo alcanza 64,16% de accuracy y ROC-AUC de 0,6981, con poca variación entre folds, pero omite aproximadamente el 37,7% de las personas sin cuenta. Estos resultados describen asociaciones, no efectos causales, y deben interpretarse dentro de la cobertura y el periodo de los datos.

Fuentes reproducibles: notebook 02; outputs/metrics/logistic_model_comparison.csv, logistic_metrics.csv, logistic_cross_validation.csv y logistic_sensitivity_specificity.csv; outputs/tables/logistic_coefficients.csv. Las métricas de este informe se derivan exclusivamente del modelo y de los folds actuales, sin cambios de hiperparámetros.


El EDA se consulta en `outputs/tables/account_by_income.csv`, `account_by_education.csv`, `account_by_mobile.csv`, `account_by_employment.csv`, `account_by_age.csv`, `account_by_gender.csv` y `account_by_country.csv`. La tabla `outputs/tables/logistic_final_summary.csv` reúne valores ya guardados y sus fuentes; las métricas se expresan en escala 0–1 y los OR son razones de odds. Esta ampliación documental no recalcula el modelo ni modifica los outputs existentes.
