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

Actualmente, el repositorio contiene solo la estructura inicial. El análisis, el entrenamiento de modelos y los resultados quedan pendientes.

## Estructura del repositorio

- `data/`: datos originales en `raw/` y datos preparados en `processed/`.
- `notebooks/`: notebooks numerados para exploración y limpieza, regresión logística, Random Forest y comparación de modelos.
- `src/`: módulos de apoyo para procesamiento de datos, evaluación y utilidades. Por ahora contienen únicamente una descripción de su propósito.
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

Coloca manualmente el dataset original de Global Findex 2017 en `data/raw/`. Si está comprimido, extrae allí los archivos que se utilizarán. Todavía no se requiere un nombre de archivo específico.

Abre Jupyter Notebook desde la raíz del repositorio:

```bash
jupyter notebook
```

También puedes abrir los archivos de `notebooks/` en JupyterLab, si lo tienes instalado, o en VS Code con las extensiones de Python y Jupyter. Selecciona el entorno `.venv` como kernel y comienza por `01_exploracion_limpieza.ipynb`.

Los notebooks contienen inicialmente solo un título y una descripción; se completarán durante el desarrollo del proyecto.
