# Brechas de inclusión financiera: factores asociados a la tenencia de cuentas en instituciones financieras

Proyecto de Ciencia de Datos — Grupo 10

## Integrantes

- Isaias Carte — Rol: 202273606-2
- Rodrigo Ramirez — Rol: [AGREGAR ROL]

## Propósito

El proyecto analizará datos de **Global Findex Database 2017 del Banco Mundial**, con foco en adultos de **América Latina y el Caribe**, para estudiar qué características sociodemográficas y de acceso tecnológico permiten predecir si una persona posee una cuenta en una institución financiera.

Se considerarán variables como edad, sexo, educación, quintil de ingreso, participación laboral y tenencia de teléfono móvil.

## Qué se realizará

1. Limpieza y exploración de los datos.
2. Análisis de brechas de inclusión financiera.
3. Modelo de regresión logística.
4. Modelo Random Forest.
5. Evaluación y comparación de ambos modelos.
6. Interpretación de las características más relevantes.

La preparación, limpieza y exploración inicial están realizadas en `notebooks/01_exploracion_limpieza.ipynb`. La base común para los futuros modelos está en `data/processed/findex_lac_clean.csv`. La regresión logística y los Random Forest base y ajustado están entrenados y evaluados en los notebooks 02 y 03. Ambos usan los mismos seis predictores y el mismo train/test guardado. La comparación final y la selección de modelo siguen pendientes.

Consulta las decisiones y los resultados descriptivos en [docs/preparacion_datos.md](docs/preparacion_datos.md).

## Estructura del repositorio

- `data/`: datos originales en `raw/` y datos preparados en `processed/`.
- `notebooks/`: notebooks numerados para exploración y limpieza, regresión logística, Random Forest y comparación de modelos.
- `src/`: módulos de apoyo para procesamiento de datos, evaluación y utilidades. Incluye funciones reutilizables de limpieza y de generación de tablas y gráficos descriptivos.
- `models/`: modelos entrenados que se guardarán en etapas posteriores.
- `outputs/`: figuras, tablas y métricas generadas durante el proyecto.
- `docs/`: documentación e informes del proyecto.

Las carpetas inicialmente vacías incluyen un archivo `.gitkeep` para conservarlas en Git. Los datos procesados y los resultados no están excluidos mediante `.gitignore`.

## Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/IsaiasACF/proyecto-ciencia-datos-findex.git
cd proyecto-ciencia-datos-findex
```

### 2. Crear un entorno virtual

Con Python 3 instalado:

```bash
python -m venv .venv
```

En Linux/macOS, utiliza `python3` si ese es el nombre del comando de Python en tu sistema.

### 3. Activar el entorno

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows (CMD):

```bat
.venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Incorporar el dataset y abrir los notebooks

El notebook utiliza `data/raw/micro_world.csv`, extraído sin modificar de `WLD_2017_FINDEX_v02_M_CSV.zip`. Si necesitas restaurarlo, extrae únicamente ese CSV dentro de `data/raw/`. Conserva también la documentación de `docs/source/`, necesaria para verificar las codificaciones sin conexión a internet. No edites el archivo original.

Abre Jupyter Notebook desde la raíz del repositorio:

```bash
jupyter notebook
```

También puedes abrir los archivos de `notebooks/` en JupyterLab, si lo tienes instalado, o en VS Code con las extensiones de Python y Jupyter. Selecciona el entorno `.venv` como kernel y comienza por `01_exploracion_limpieza.ipynb`.

Ejecuta todas las celdas de `01_exploracion_limpieza.ipynb` en orden para regenerar el dataset procesado, las siete figuras y las tablas. El notebook admite ejecutarse desde la raíz del repositorio o desde `notebooks/`; utiliza rutas relativas. El notebook 02 implementa la regresión logística, su baseline y la interpretación de coeficientes. El notebook 03 implementa el Random Forest base y una búsqueda de hiperparámetros con cinco folds exclusivamente en entrenamiento. El modelo ajustado se guarda como `models/random_forest_tuned.joblib` y sus salidas usan el prefijo `random_forest_tuned_`; se conserva el split original. El notebook 04 conserva únicamente su título y descripción para la comparación final.

Para ejecutar la exploración completa desde la raíz mediante la terminal, con el entorno activado:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploracion_limpieza.ipynb
```

Los descriptivos distinguen porcentajes muestrales y ponderados. El alcance incluye 20 economías geográficas de América Latina y el Caribe, con inclusión explícita de Chile, Uruguay y Trinidad y Tobago, clasificados por ingreso alto en `regionwb`. La regresión logística usa una partición estratificada 80/20 (`random_state=42`), sin país ni pesos muestrales. El notebook 02 guarda las métricas y predicciones de prueba en `outputs/metrics/`, los coeficientes y los índices de partición en `outputs/tables/`, tres gráficos en `outputs/figures/` y la pipeline ajustada en `models/logistic_regression.joblib`.


Para regenerar la regresión logística desde la raíz, utilizando la base limpia validada:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/02_regresion_logistica.ipynb
```

Las referencias categóricas y el centrado de edad están documentados en ese notebook. La huella del dataset, las versiones del entorno y los parámetros usados se conservan en `outputs/metrics/logistic_run_info.json`. La ejecución del notebook 02 sobrescribe únicamente sus propios resultados y la tabla de partición; no modifica el dataset limpio ni ejecuta otros modelos.
