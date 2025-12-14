# Steam Games Data Engineering Pipeline

> **Data Pipeline & ETL Project** | Designed and developed as part of **Soy Henry Bootcamp** following production-level data engineering practices

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura de Datos](#arquitectura-de-datos)
- [Pipeline ETL](#pipeline-etl)
- [Stack Tecnológico](#stack-tecnológico)
- [Funciones de Datos (API Endpoints)](#funciones-de-datos-api-endpoints)
- [Guía de Instalación](#guía-de-instalación)
- [Deployment](#deployment)

---

## 📊 Descripción General

Proyecto de **Ingeniería de Datos** enfocado en el diseño e implementación de un pipeline ETL (Extract, Transform, Load) completo para un dataset de videojuegos de Steam.

**Objetivo Principal:**
- Extraer datos crudos de múltiples fuentes
- Aplicar transformaciones y limpieza de datos (ETL)
- Modelar datos en una estructura relacional optimizada
- Exponer datos transformados mediante API REST para consumo por aplicaciones y dashboards
- Implementar un sistema de recomendación basado en el modelo de datos

**Logros Clave:**
- ✅ Pipeline ETL automatizado que procesa y transforma datos de videojuegos
- ✅ Modelado de datos relacional con normalización y optimización de consultas
- ✅ 6 endpoints de datos que exponen KPIs y análisis agregados
- ✅ API REST con FastAPI para acceso a datos procesados
- ✅ Análisis Exploratorio de Datos (EDA) para calidad de datos
- ✅ Sistema de recomendación con predicción de precios
- ✅ Deployment productivo con Render

---

## 🏗️ Arquitectura de Datos

```
┌─────────────────┐
│  Datos Crudos   │
│ (CSV, JSON)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  EXTRACTION & VALIDATION    │
│  - Lectura de datos         │
│  - Validación de esquema    │
│  - Detección de anomalías   │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  TRANSFORMATION             │
│  - Limpieza de valores NULL │
│  - Normalización de datos   │
│  - Ingeniería de features   │
│  - Conversión de tipos      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  LOAD TO DATABASE           │
│  - Modelado relacional      │
│  - Tablas normalizadas      │
│  - Índices optimizados      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  DATA EXPOSURE LAYER        │
│  - API REST (FastAPI)       │
│  - 6 endpoints de datos     │
│  - Vistas agregadas         │
└─────────────────────────────┘
```

---

## 🔄 Pipeline ETL

### 1. **Extract (Extracción)**
- Lectura de archivos CSV y JSON
- Validación de integridad de datos
- Detección de valores atípicos y missing data

### 2. **Transform (Transformación)**
Transformaciones aplicadas en el notebook EDA.ipynb y reflejadas en el pipeline:
- **Limpieza**: Eliminación y tratamiento de NULL values
- **Normalización**: Conversión de tipos de datos
- **Feature Engineering**: Creación de nuevas columnas derivadas
- **Validación de calidad**: Chequeos de integridad referencial

### 3. **Load (Carga)**
- Carga de datos transformados a base de datos relacional
- Creación de tablas normalizadas
- Establecimiento de relaciones y constraints
- Índices para optimización de consultas

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| **Lenguaje** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) |
| **Data Analysis** | ![Jupyter](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) Seaborn, Matplotlib |
| **API & Web** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) |
| **ML & Modeling** | ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) |
| **Version Control** | ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) |
| **Deployment** | ![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white) |
| **IDE** | ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) |

---

## 📡 Funciones de Datos (API Endpoints)

API REST que expone datos procesados y agregaciones para consumo por dashboards y aplicaciones frontend.

### 1. **Top 5 Géneros por Año**
```
GET /generos_año?año={año}
```
Retorna los 5 géneros más vendidos en un año específico ordenados por volumen de ventas.
- **Input**: Año (int)
- **Output**: Lista de géneros con métricas de venta

### 2. **Juegos Lanzados por Año**
```
GET /juegos_año?año={año}
```
Retorna el listado completo de videojuegos lanzados en un año determinado.
- **Input**: Año (int)
- **Output**: Array de juegos con metadatos

### 3. **Top 5 Especificaciones Técnicas**
```
GET /specs_año?año={año}
```
Retorna los 5 specs (características técnicas) más frecuentes en lanzamientos de un año.
- **Input**: Año (int)
- **Output**: Top 5 especificaciones ordenadas por frecuencia

### 4. **Juegos con Early Access**
```
GET /early_access?año={año}
```
Retorna cantidad de juegos lanzados en early access en un año específico.
- **Input**: Año (int)
- **Output**: Cantidad total y lista de juegos

### 5. **Análisis de Sentimiento por Año**
```
GET /sentimiento?año={año}
```
Retorna distribución de análisis de sentimiento de reviews por año.
- **Input**: Año (int)
- **Output**: Categorización de sentimientos con conteos

### 6. **Top 5 Juegos por Metascore**
```
GET /top_metascore?año={año}
```
Retorna los 5 videojuegos con mayor metascore (puntuación de crítica) en un año.
- **Input**: Año (int)
- **Output**: Top 5 juegos ordenados por metascore descendente

---

## 📈 Análisis Exploratorio de Datos (EDA)

El notebook `EDA.ipynb` contiene:
- **Estadísticas descriptivas**: Media, mediana, desviación estándar de variables clave
- **Análisis de distribuciones**: Histogramas y boxplots para detección de outliers
- **Correlaciones**: Matriz de correlación entre variables numéricas
- **Anomalías**: Identificación de valores atípicos y missing data
- **Validaciones**: Chequeos de integridad referencial y calidad de datos

---

## 🤖 Sistema de Recomendación

Sistema basado en **content-based filtering** que predice precios de videojuegos usando:
- **Características utilizadas**: Año de lanzamiento, metascore, acceso anticipado
- **Modelo**: Regresión con scikit-learn
- **Métrica**: RMSE (Root Mean Squared Error) para evaluación
- **Integración**: Consumido por la API REST para pruebas en tiempo real

---

## 📦 Guía de Instalación

### Requisitos Previos
- Python 3.8+
- pip
- Git

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/franco18min/Machine-Learning-Operations-MLOps.git
cd Machine-Learning-Operations-MLOps

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el ETL
python main.py

# 5. Iniciar API FastAPI
uvicorn main:app --reload
```

### Dependencias Principales
Ver archivo `requirements.txt` para lista completa.

---

## 🚀 Deployment

**Plataforma**: Render  
**Tipo**: Web Service  
**Status**: Activo

La API se encuentra desplegada y disponible en producción. Todas las funciones están optimizadas para latencia baja y alta disponibilidad.

---

## 📚 Estructura del Proyecto

```
Machine-Learning-Operations-MLOps/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias del proyecto
├── main.py                   # Script principal ETL y API
├── model.py                  # Modelo de recomendación
├── EDA.ipynb                # Análisis Exploratorio de Datos
├── steam_games.csv          # Dataset crudo (CSV)
├── steam_games.json         # Dataset crudo (JSON)
└── .vscode/                 # Configuración VS Code
```

---

## 🎓 Contexto: Soy Henry Bootcamp

Este proyecto fue desarrollado como parte del programa **Soy Henry**, un bootcamp intensivo de Data Science e Ingeniería de Datos. Durante la cursada, se aplicaron prácticas profesionales de:
- Diseño de pipelines ETL robustos
- Modelado de datos relacional
- Buenas prácticas de código y versionado (Git)
- Deployment y productivización de soluciones

**Competencias desarrolladas**:
✅ ETL y Data Processing  
✅ SQL y Base de Datos Relacionales  
✅ Python (Pandas, NumPy, scikit-learn)  
✅ API REST (FastAPI)  
✅ Análisis Exploratorio de Datos  
✅ Machine Learning (Regresión)  
✅ Git & GitHub  
✅ Deployment & DevOps básico  

---

## 👤 Autor

**Franco Min**  
Data Engineer | Soy Henry Graduate  
[GitHub](https://github.com/franco18min) | [LinkedIn](#)

---

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT. Libre para uso educativo y profesional.
