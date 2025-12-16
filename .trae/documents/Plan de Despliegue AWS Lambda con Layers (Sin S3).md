# Despliegue Optimizado sin Costos (Zero-Cost Deployment)

## Estrategia: AWS Lambda Layers
Para evitar el uso de almacenamiento S3 y reducir el tamaño del paquete de despliegue (que causó el error anterior), utilizaremos capas (Layers) preconstruidas de AWS.

## Pasos de Implementación:

### 1. Limpieza y Re-empaquetado
*   Eliminar las librerías pesadas (`pandas`, `numpy`, etc.) del directorio local de despliegue.
*   Crear un nuevo archivo `lambda_deployment.zip` ultra-ligero que solo contenga:
    *   `lambda_function.py` (Lógica)
    *   `steam_games.csv` (Datos)

### 2. Actualizar Script de Despliegue (`deploy_lambda.ps1`)
*   **Eliminar**: Comandos de creación y subida a S3 (`aws s3 mb`, `aws s3 cp`).
*   **Modificar**: Comando `aws lambda create-function` para usar subida directa.
*   **Agregar**: Parámetro `--layers` con el ARN oficial de AWS para Data Wrangler (Pandas/Numpy) en Python 3.11.
    *   ARN: `arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:12`

### 3. Ejecución
*   Correr el script para desplegar directamente.

**Resultado Esperado**:
*   Despliegue exitoso sin errores de tamaño.
*   Cero costos de almacenamiento S3.
*   Funcionalidad completa de ETL en la nube.