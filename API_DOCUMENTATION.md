# 🌐 Steam Games API Documentation

API Serverless desplegada en AWS Lambda utilizando **Function URL** (Capa gratuita). Provee acceso a datos de juegos de Steam almacenados en DynamoDB.

**Base URL**:  
`https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/`

---

## 🚀 Endpoints

### 1. Health Check
Verifica el estado de la API y lista los endpoints disponibles.

*   **URL**: `/`
*   **Método**: `GET`
*   **Ejemplo**:
    ```bash
    curl "https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/"
    ```

### 2. Top Juegos (Más Caros)
Devuelve el top 10 de juegos con mayor precio.

*   **URL**: `/?top=true`
*   **Método**: `GET`
*   **Ejemplo**:
    ```bash
    curl "https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/?top=true"
    ```

### 3. Juegos por Género
Filtra juegos que contengan el género especificado.

*   **URL**: `/?genre={Genero}`
*   **Método**: `GET`
*   **Parámetros**:
    *   `genre` (string): Género a buscar (ej. `Action`, `RPG`, `Indie`).
*   **Ejemplo**:
    ```bash
    curl "https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/?genre=Action"
    ```

### 4. Juegos por Año
Filtra juegos lanzados en un año específico.

*   **URL**: `/?year={YYYY}`
*   **Método**: `GET`
*   **Parámetros**:
    *   `year` (int): Año de lanzamiento.
*   **Ejemplo**:
    ```bash
    curl "https://telly66645uoeanoolnr3l4x2u0aaevi.lambda-url.us-east-1.on.aws/?year=2017"
    ```

---

## 🛠️ Arquitectura

*   **Compute**: AWS Lambda (Python 3.11)
*   **Database**: AWS DynamoDB (On-demand)
*   **ETL**: Lambda con Pandas Layer (carga desde CSV)
*   **Infraestructura**: Despliegue automatizado con PowerShell y AWS CLI.

## 💰 Costos
*   **API Gateway**: Reemplazado por Lambda Function URL ($0.00).
*   **Lambda**: Capa gratuita (400,000 GB-segundos / mes).
*   **DynamoDB**: Capa gratuita (25 GB almacenamiento).
*   **S3**: No utilizado (despliegue directo).

**Costo Total Estimado: $0.00 / mes**
