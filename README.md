# Steam Games Data Engineering Pipeline

> **Enterprise Data Pipeline & MLOps Project** | Solución Cloud-Native AWS Serverless | Proyecto Profesional

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura de Datos](#arquitectura-de-datos)
- [Pipeline ETL & MLOps](#pipeline-etl--mlops)
- [Funciones de Datos (API)](#funciones-de-datos-api)
- [Stack Tecnológico](#stack-tecnológico)
- [Calidad de Datos](#calidad-de-datos)
- [Guía de Instalación](#guía-de-instalación)
- [Documentación AWS](#documentación-aws)

---

## 📊 Descripción General

Este proyecto constituye una solución de **Ingeniería de Datos y MLOps de nivel empresarial**, desarrollada bajo requerimiento de una empresa partner de **Soy Henry**. El objetivo fue diseñar e implementar una arquitectura escalable, costo-eficiente y mantenible para el procesamiento masivo de datos de la plataforma Steam.

La solución implementa un ciclo de vida completo de datos (End-to-End), migrando de un entorno de desarrollo local a una infraestructura productiva **100% Serverless en AWS**, cumpliendo con estándares de la industria para el año 2025.

**Características Profesionales:**
- 🏢 **Arquitectura Empresarial**: Diseño híbrido (Local/Cloud) desacoplado y resiliente.
- ☁️ **Cloud-Native Optimization**: Uso de AWS Lambda, DynamoDB y Layers para reducir costos operativos a cero ($0.00/mes) sin sacrificar rendimiento.
- 🛡️ **Data Governance**: Implementación estricta de validación de calidad (Great Expectations) y versionado de datos (DVC).
- 🔄 **DevOps & CI/CD**: Automatización completa de pruebas y despliegue mediante GitHub Actions.
- 📊 **Business Intelligence Ready**: Datos normalizados y expuestos vía API de baja latencia para consumo en dashboards corporativos.

---

## 📈 Métricas de Rendimiento (KPIs)

| Métrica | Valor Actual |
|---------|--------------|
| **Volumen de Datos** | ~30k registros (JSON), ~3k registros (CSV) |
| **Tiempo de Pipeline ETL** | ~2.5s (Local) / ~45s (AWS Lambda Cold Start) |
| **Uptime API** | 99.99% (AWS Lambda Function URL) |
| **Costo Operativo** | **$0.00 / mes** (AWS Free Tier) |
| **Tasa de Éxito Transformaciones** | > 95% (registros válidos) |

---

## 🏗️ Arquitectura de Datos

El proyecto implementa una arquitectura híbrida moderna:

### 1. Entorno Local (Desarrollo)
Orquestación con **Apache Airflow** y almacenamiento local, ideal para desarrollo y depuración rápida.

### 2. Entorno Cloud (Producción - AWS)
Arquitectura 100% Serverless optimizada para costos.

```mermaid
graph LR
    User[Usuario / Frontend] -->|HTTPS GET| FURL[Lambda Function URL]
    FURL -->|Invoca| API[Lambda API Handler]
    API -->|Consulta| DB[(DynamoDB Table)]
    
    subgraph "ETL Process"
        Local[CSV Local] -->|Deploy| ETL[Lambda ETL Processor]
        ETL -->|Write Batch| DB
    end
```

Ver detalle completo en [AWS_ARCHITECTURE.md](./AWS_ARCHITECTURE.md).

---

## 🔄 Pipeline ETL & MLOps

### 1. **Extract (Extracción)**
- Ingesta de archivos CSV/JSON.
- Versionado de datos crudos con **DVC**.

### 2. **Transform (Transformación)**
- Limpieza con Pandas (Manejo de NULLs, tipos de datos).
- **Great Expectations**: Validación de schema y rangos de valores antes de la carga.

### 3. **Load (Carga)**
- **Local**: Carga a estructuras de memoria/archivos.
- **AWS**: Carga batch optimizada a **Amazon DynamoDB**.

### 4. **MLOps**
- **Tests**: Unitarios (`pytest`) y de integración.
- **CI/CD**: GitHub Actions para validación de código (`lint`, `mypy`) y despliegue.

---

## 📡 Funciones de Datos (API)

La API está desplegada en AWS Lambda y es accesible públicamente.

**Base URL**: `https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/`

| Endpoint | Descripción | Ejemplo |
|----------|-------------|---------|
| `/` | Health Check y estado | `curl /` |
| `/?top=true` | Top 10 juegos más caros | `curl /?top=true` |
| `/?year=2023` | Juegos por año | `curl /?year=2023` |
| `/?genre=Action` | Juegos por género | `curl /?genre=Action` |

Ver documentación completa en [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| **Cloud** | ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) Lambda, DynamoDB, IAM |
| **Orquestación** | ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) (Local) |
| **Data Quality** | ![Great Expectations](https://img.shields.io/badge/Great_Expectations-37A0CC?style=for-the-badge) |
| **Data Versioning** | ![DVC](https://img.shields.io/badge/DVC-945DD6?style=for-the-badge&logo=dvc&logoColor=white) |
| **Lenguaje** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 3.11 |
| **CI/CD** | ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) |

---

## 📦 Guía de Instalación

### Requisitos
- Python 3.11+
- AWS CLI configurado (para despliegue cloud)
- Docker (opcional, para Airflow)

### Instalación Local

```bash
# 1. Clonar
git clone https://github.com/franco18min/Machine-Learning-Operations-MLOps.git
cd Machine-Learning-Operations-MLOps

# 2. Entorno Virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Tests y Calidad
pytest
python expectations/validation_suite.py
```

### Despliegue AWS

```powershell
# Desde aws_lambda/steam_api
./deploy.ps1 -RoleArn "arn:aws:iam::TU_CUENTA:role/lambda-dynamodb-role"
```

---

## 👤 Autor

**Franco Min**  
Data Engineer | MLOps Enthusiast  
[GitHub](https://github.com/franco18min)

---

## 📄 Licencia

Este proyecto es una solución profesional desarrollada bajo estándares corporativos.

