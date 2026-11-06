# Preparación y exploración de datos — Grupo 10

Se trabajó exclusivamente en la primera fase. El notebook `01_exploracion_limpieza.ipynb` regenera las tablas, figuras y la base común; no entrena modelos, no divide datos ni calcula métricas de clasificación.

## Fuente y cobertura

Original: `data/raw/micro_world.csv`, extraído de `WLD_2017_FINDEX_v02_M_CSV.zip`, versión `WLD_2017_FINDEX_v02_M`. Contiene **154.923 filas y 105 columnas**, correspondientes a 144 economías. Los ZIP originales se conservaron fuera del repositorio. Solo se extrajo el CSV necesario; del ZIP ASCII se conservaron las sintaxis SPSS/SAS en `docs/source/`, sin extraer el DAT. La huella del CSV se verifica al ejecutar el notebook.

El filtro puramente textual de `regionwb` arroja **16.504 observaciones**. Ese grupo excluye ingresos altos. Para seguir el alcance geográfico del proyecto se incorporaron explícitamente **Chile, Uruguay y Trinidad y Tobago**, con lo que se obtuvieron **19.048 observaciones de 20 economías**. No se alteró la clasificación original.

Economías: Argentina, Bolivia, Brasil, Chile, Colombia, Costa Rica, República Dominicana, Ecuador, El Salvador, Guatemala, Haití, Honduras, México, Nicaragua, Panamá, Paraguay, Perú, Trinidad y Tobago, Uruguay y Venezuela. La cobertura del Caribe es parcial; no se agregan economías sin datos. `lac_economies.csv` registra la lista y el criterio; `region_economy_audit.csv` permite revisar las inclusiones y exclusiones del archivo completo.

## Codificación y limpieza

Se contrastaron las frecuencias del CSV con los [metadatos oficiales de 2017](https://microdata.worldbank.org/metadata/export/3324/json), conservados localmente, y las etiquetas con las sintaxis adjuntas.

- `female`: 1 = Hombre; 2 = Mujer.
- `educ`: 1 = Primaria o menos; 2 = Secundaria; 3 = Terciaria o más; 4 = dk y 5 = rf se convierten en faltantes.
- `inc_q`: quintiles 1–5, relativos a cada economía.
- `emp_in`: 0 = Fuera de fuerza laboral; 1 = En fuerza laboral.
- `mobileowner`: 1 = Tiene teléfono; 2 = No tiene teléfono; 3 = dk y 4 = rechazo se convierten en faltantes.
- `age`: se conserva el rango documentado de 15 a 99; 99 significa 99 o más. En LAC hay seis registros 99+; no se eliminan edades altas.

**Objetivo validado:** la definición oficial de indicadores de 2017 establece `account_fin = 1` cuando la persona cumple alguno de los criterios de tenencia de cuenta y **0 en caso contrario**. La falta de etiqueta del 0 en el catálogo no impide interpretar el indicador: la definición oficial resuelve esa ambigüedad. Las etiquetas 1/2/3 de la sintaxis SPSS/SAS no corresponden a los valores efectivos del archivo. El CSV y el DAT del ZIP contienen exactamente los mismos valores 0/1, sin discrepancias en las 154.923 filas. La construcción y los límites de la reconstrucción independiente se detallan en la sección de verificaciones adicionales. No se modificó ni recodificó el objetivo.

En LAC se detectaron **18 edades faltantes**, **72 no respuestas educativas** (49 dk y 23 rf) y **34 no respuestas sobre teléfono** (12 dk y 22 rechazos). Hay superposición entre estas filas: la eliminación conjunta alcanza **121 personas (0,6352%)**. No hubo faltantes en los demás campos seleccionados. Se descartaron casos incompletos en el objetivo y los seis predictores, sin imputaciones; el umbral operativo de revisión se fijó en 5%. La pérdida pequeña no garantiza ausencia de sesgo de selección. La mayor pérdida por economía corresponde a República Dominicana: 47 de 1.000 casos (4,7%); conviene revisar ese patrón antes de modelar.

Base final: **18.927 filas y 11 columnas**, en `data/processed/findex_lac_clean.csv`: objetivo, seis predictores y `economy`, `economycode`, `regionwb`, `wgt`. Se conservan los códigos válidos originales; no contiene etiquetas visuales, población adulta ni pesos descriptivos derivados. Ambos modelos deberán cargar este mismo CSV.

## Pesos y resultados descriptivos

`wgt` es positivo y está completo en LAC; sus sumas equivalen aproximadamente a la cantidad de entrevistas de cada economía. Se usa para proporciones por país, de acuerdo con la [metodología 2017](https://thedocs.worldbank.org/en/doc/d4be0980516591d047aeb1945eab6598-0050062022/original/Methodology2017.pdf).

Para las proporciones conjuntas se emplea `wgt × pop_adult_pais / suma_wgt_original_pais`. `pop_adult` es población 15+ de 2016 (WDI), constante por país en el original; las referencias se calculan antes de eliminar casos. Esto combina el ajuste dentro de los países con su población adulta, siguiendo el principio de [ponderación poblacional de agregados regionales](https://worldbank.github.io/sdg-metadata/metadata/en/8-10-2/). Los pesos derivados solo se usan en memoria y las referencias quedan en `weight_summary_by_country.csv`.

Los resultados posteriores a limpiar están condicionados a casos completos y no se recalibran por no respuesta. Se refieren a las economías cubiertas, no son un agregado oficial de toda LAC. No se estiman errores estándar del diseño complejo ni intervalos de confianza.

| Clase | Personas en la muestra final | Porcentaje no ponderado | Porcentaje ponderado regional |
|---|---:|---:|---:|
| Con cuenta | 9.490 | 50,14% | 54,45% |
| Sin cuenta | 9.437 | 49,86% | 45,55% |

No se observa desbalance marcado de clases en la muestra. Antes de eliminar casos, la proporción con cuenta era 50,09% no ponderada y 54,25% ponderada regional; después es 50,14% y 54,45%, respectivamente.

Principales asociaciones observadas en los casos completos (porcentajes conjuntos ponderados con `wgt` y población adulta):

- Ingreso: 38,96% con cuenta en quintil 1 frente a 73,78% en quintil 5; los porcentajes aumentan entre quintiles.
- Educación: 43,82% en primaria o menos, 56,87% en secundaria y 77,55% en terciaria o más.
- Sexo: 57,72% en hombres y 51,50% en mujeres.
- Fuerza laboral: 59,55% dentro frente a 43,50% fuera.
- Teléfono: 59,97% entre quienes poseen teléfono frente a 33,43% entre quienes no.
- Edad: 38,55% entre 15–24 años; los grupos 25–34 y 35–44 muestran alrededor de 62% y 61%. La relación no es creciente a lo largo de todos los grupos etarios.
- Por economía, ponderando **solo con `wgt` dentro del país**, la proporción va de 28,07% en Haití a 80,84% en Trinidad y Tobago: una amplitud de 52,76 puntos porcentuales.

Son diferencias marginales y asociaciones; no prueban causalidad ni permiten ordenar la relevancia predictiva de las variables. La heterogeneidad geográfica requiere atención, pero no demuestra que el país explique más que los factores individuales.

## Archivos y reproducción

- Modificados: `README.md`, `notebooks/01_exploracion_limpieza.ipynb`, `src/data_processing.py` y `src/utils.py`.
- Datos: CSV original intacto y CSV procesado común.
- Salidas: siete PNG en `outputs/figures/` y 22 CSV en `outputs/tables/`, incluidos los nueve mínimos solicitados, la tabla por edad, controles de codificación, faltantes, limpieza y pesos.
- Documentación: esta nota, sintaxis y fuentes en `docs/source/`, manifest de extracción, versiones de ejecución y huellas SHA-256 de los artefactos.
- Sin cambios en notebooks 02–04, `src/evaluation.py`, dependencias o reglas de exclusión. Sin commits ni push.

Con las dependencias de `requirements.txt` instaladas, ejecutar desde la raíz:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploracion_limpieza.ipynb
```

El notebook usa rutas relativas y fuentes locales. `docs/exploration_environment.json` registra las versiones usadas; las huellas en `docs/exploration_artifacts_sha256.json` permiten comparar artefactos al repetir la ejecución con el mismo entorno.

Se ejecutó el notebook completo con dos kernels nuevos, primero desde `notebooks/` y luego desde la raíz: 25 celdas de código ejecutadas en cada ocasión, sin errores. Los 30 artefactos (dataset procesado, 22 tablas y siete figuras) resultaron idénticos por SHA-256. El registro está en `docs/exploration_validation.json`. Se comprobó también que el CSV original conserva su huella y que los otros notebooks permanecen sin cambios.

## Revisar antes de la regresión logística

Se mantiene el alcance geográfico de 20 economías, incluida la incorporación explícita de Chile, Uruguay y Trinidad y Tobago. La definición oficial confirma 0/1 de `account_fin`; sigue pendiente una reconstrucción completa e independiente, porque no se publican todas las variables fuente necesarias. La comparación de República Dominicana no muestra un cambio importante en la distribución del objetivo tras limpiar, aunque no descarta sesgos respecto de otras características. Decidir después la codificación de categorías y edad 99+, la ponderación del modelamiento y una evaluación que considere país. No se decidió ni implementó una partición de datos. La fase de modelos queda pendiente de revisión.


## Verificaciones adicionales antes del modelamiento

### 1. Inclusión geográfica de Chile, Uruguay y Trinidad y Tobago

Se confirmó que el filtro mantiene las tres economías. La decisión es **geográfica**, no una reclasificación por ingreso:

| Economía | Código | `regionwb` original | Filas antes de limpiar | Filas finales |
|---|---|---|---:|---:|
| Chile | CHL | High income: OECD | 1.040 | 1.038 |
| Uruguay | URY | High income: nonOECD | 1.000 | 996 |
| Trinidad y Tobago | TTO | High income: nonOECD | 504 | 490 |

Se conserva `regionwb` tal como fue publicado. La selección completa sigue siendo de 19.048 personas en 20 economías y la base final sigue teniendo 18.927 personas. No se modificó la función de selección ni el dataset procesado.

### 2. República Dominicana: eliminadas frente a conservadas

Se aplicó exactamente el criterio vigente: faltante en el objetivo o cualquiera de los seis predictores, después de recodificar las no respuestas documentadas. De los 47 casos eliminados, 45 carecen de educación válida y dos carecen de edad, sin superposición entre estos motivos. La comparación se realizó usando los índices del original, sin enlazar personas por coincidencia de características.

| Grupo | Personas | % de las 1.000 originales | Con cuenta (1) | Sin cuenta (0) | % con cuenta dentro del grupo | % sin cuenta dentro del grupo |
|---|---:|---:|---:|---:|---:|---:|
| Original | 1.000 | 100,0% | 519 | 481 | 51,90% | 48,10% |
| Conservadas | 953 | 95,3% | 496 | 457 | 52,05% | 47,95% |
| Eliminadas | 47 | 4,7% | 23 | 24 | 48,94% | 51,06% |

Los conteos y porcentajes anteriores son **no ponderados**. El porcentaje con cuenta entre conservadas supera al de eliminadas en **3,11 puntos porcentuales**, pero al excluir solo el 4,7% de la muestra la proporción total pasa de 51,90% a 52,05%: **+0,146 puntos porcentuales**.

Como comprobación descriptiva adicional, usando **`wgt` dentro del país**, el porcentaje con cuenta es 54,783% en el original, 55,075% entre conservadas y 48,578% entre eliminadas. El cambio de la estimación original a la final es **+0,292 puntos porcentuales**. Los porcentajes ponderados no sustituyen los conteos muestrales.

**Conclusión:** la eliminación no parece introducir un sesgo evidente o de gran magnitud en la distribución marginal de `account_fin`, aunque se pierde ligeramente más representación de personas sin cuenta. Los 47 casos no permiten demostrar ausencia de sesgo y esta comparación no evalúa posibles cambios en asociaciones con los predictores. La concentración de pérdidas en educación sigue siendo una limitación. Se mantiene la limpieza, ya que no se encontró un problema importante que justifique cambiarla.

### 3. Construcción y validación de `account_fin`

**Fuentes examinadas.** Se revisaron los dos ZIP locales y las sintaxis `micro_world.sps`/`.sas`; el CSV y el DAT se contrastaron sin modificar ni extraer el DAT. El ZIP CSV solo contiene el CSV, y el ZIP ASCII contiene DAT, SPSS y SAS: no contienen la sintaxis de construcción original de `account_fin`. Además se revisó íntegramente la copia oficial de [Micro17 indicators.do](https://microdata.worldbank.org/catalog/3324/download/44605), comprobando que la copia local coincide byte por byte con la descargada. Se incorporaron como fuentes locales las [definiciones de indicadores 2017](https://microdata.worldbank.org/catalog/3324/download/44601), el [glosario 2017](https://microdata.worldbank.org/catalog/3324/download/44604) y el [cuestionario 2017](https://microdata.worldbank.org/catalog/3324/download/44599).

**Definición y significado de los códigos.** La primera entrada de `Indicator_definitions_2017.pdf` establece explícitamente 1 cuando se cumple un criterio de tenencia y 0 en caso contrario. El indicador combina declaración de cuenta individual o conjunta, débito ligado a una cuenta a nombre propio y evidencia de recibir ciertos pagos o realizar ciertos pagos desde una cuenta. Incluye salarios, transferencias, pensión pública, pagos agrícolas y pagos de servicios o educación. El glosario complementa los criterios incluyendo salarios y transferencias recibidos en tarjeta. Por tanto, es un **indicador construido**, no una copia de la respuesta directa a FIN1. El 0 significa que no se cumplen los criterios afirmativos documentados; no es el código 2 de la pregunta original. Esto resuelve la ambigüedad de la etiqueta vacía del 0 mencionada en la primera revisión, sin permitir recuperar el tratamiento individual de no respuestas en las fuentes no publicadas.

**Qué hace realmente Micro17 indicators.do.** El script construye indicadores de pagos (`receive_wages`, `receive_transfers`, `receive_pension`, `receive_agriculture`, `pay_utilities`) y remesas. **No contiene `gen account_fin` ni `replace account_fin`: la variable ya debe existir.** La expresión `account_fin != .` de varias líneas verifica que no falte el valor y admite tanto 0 como 1; no equivale a `account_fin == 1`. Por ello, ejecutar ese script o invertir sus indicadores de pagos no reconstruye el objetivo y podría introducir una comprobación circular.

**Fuentes originales y posibilidad de reconstrucción.** FIN1 es la declaración directa de cuenta y aparece en el cuestionario, pero **`fin1` no está en el CSV ni en el esquema SPSS/SAS del DAT**. FIN2 identifica tarjeta de débito y FIN3 que la cuenta asociada está a nombre de la persona. FIN31A, FIN34A/FIN34C2, FIN39A/FIN39C2 y FIN43A aportan evidencia de pagos de servicios, salarios, transferencias/pensiones y pagos agrícolas. No se identifica una columna explícita de pagos escolares entre las 105 publicadas. La ausencia de FIN1, además de no disponer del programa que creó el objetivo, impide una reconstrucción completa e independiente para todas las personas. No se infieren respuestas faltantes a partir del propio objetivo ni se declaran cero discrepancias de una reconstrucción que no puede realizarse.

Se hizo una **comprobación parcial fila por fila** con condiciones afirmativas documentadas presentes: `fin3 == 1` **o** cualquiera de `fin31a`, `fin34a`, `fin34c2`, `fin39a`, `fin39c2`, `fin43a` igual a 1. Esta regla solo confirma positivos; su valor falso no significa ausencia de cuenta, porque falta FIN1 y no se cubren todas las rutas originales.

| Ámbito | Filas revisadas | Positivos confirmados por fuentes disponibles | Contradicciones: fuente afirmativa y `account_fin = 0` | `account_fin = 1` no explicados por la regla parcial |
|---|---:|---:|---:|---:|
| Archivo mundial | 154.923 | 81.353 | 0 | 11.572 |
| LAC antes de limpiar | 19.048 | 8.160 | 0 | 1.382 |

Si se utilizara indebidamente esa regla parcial como reconstrucción completa, resultaría en **11.572 discrepancias mundiales y 1.382 en LAC**, todas por positivos del objetivo no identificados por las fuentes parciales. **No son errores demostrados de `account_fin`**: faltan fuentes para verificar esas personas. No se consideran equivalentes a cuenta todos los pagos en tarjeta ni todas las respuestas financieras afirmativas; solo se usan los criterios documentados indicados.

Comprobaciones adicionales:

- **CSV frente a DAT original:** 154.923 valores de `account_fin` comparados en el mismo orden; **0 discrepancias**. El DAT también contiene 61.998 ceros y 92.925 unos. Las etiquetas SPSS/SAS 1/2/3 no describen sus valores efectivos.
- **Identidad del indicador de cuenta total:** `account == ((account_fin == 1) | (account_mob == 1))` en las 154.923 filas; **0 discrepancias**. Es consistencia entre indicadores publicados, no reconstrucción independiente del objetivo.
- **Reconstrucción completa desde todas las fuentes:** no realizable con los archivos disponibles; número de discrepancias completas **no determinable**. Para completarla se requiere FIN1 y la sintaxis original de construcción, y aclarar cualquier otra fuente no publicada.

Las cifras exactas y los criterios se registran en `docs/verificaciones_fase1.json`; los enlaces y las huellas de las nuevas fuentes se agregaron a `docs/source/web_sources.json`. La base limpia conserva su SHA-256 anterior: `7695ea41b4cc06354ce1409fcb1719c9b9228a1923c0f849aee4b606bf2d7aa7`. No se cambiaron la limpieza, los notebooks ni los modelos.
