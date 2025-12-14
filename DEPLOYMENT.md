# Guía de Despliegue (Deployment)

Este documento detalla los pasos necesarios para desplegar la API de Steam Games MLOps en un entorno local o servidor.

## Requisitos Previos

*   **Sistema Operativo**: Windows, macOS o Linux.
*   **Python**: Versión 3.8 o superior.
*   **Git**: Para clonar el repositorio.

## Pasos Reproducibles para Deploy

Sigue estos pasos para poner en marcha la aplicación:

1.  **Clonar el repositorio**
    ```bash
    git clone <url-del-repositorio>
    cd Machine-Learning-Operations-MLOps
    ```

2.  **Crear un entorno virtual (Recomendado)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Verificar los datos**
    Asegúrate de que los archivos `steam_games.json` y `steam_games.csv` estén presentes en la raíz del directorio del proyecto.

5.  **Ejecutar la aplicación**
    Utiliza `uvicorn` para lanzar el servidor ASGI:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    *   `--reload`: Habilita el reinicio automático al cambiar código (útil para desarrollo).
    *   `--host 0.0.0.0`: Permite el acceso desde otras máquinas en la red.

6.  **Verificar el despliegue**
    Abre tu navegador y navega a:
    *   Documentación interactiva: `http://localhost:8000/docs`
    *   Documentación alternativa: `http://localhost:8000/redoc`

## Variables de Entorno

Actualmente, el proyecto **no requiere variables de entorno** específicas para su configuración básica. Los paths a los archivos de datos están hardcodeados en el código (`main.py` y `model.py`).

*Nota: En un entorno de producción real, se recomienda mover rutas de archivos y configuraciones sensibles a variables de entorno.*

## Troubleshooting Común

### 1. Error: `ModuleNotFoundError: No module named 'fastapi'` (o similar)
*   **Causa**: Las dependencias no se instalaron correctamente o el entorno virtual no está activado.
*   **Solución**: Verifica que el entorno virtual esté activo (prompt debe mostrar `(venv)`) y ejecuta `pip install -r requirements.txt` nuevamente.

### 2. Error: `FileNotFoundError: [Errno 2] No such file or directory: 'steam_games.json'`
*   **Causa**: La aplicación no encuentra los archivos de datos.
*   **Solución**: Asegúrate de estar ejecutando el comando `uvicorn` desde la raíz del proyecto (donde están los archivos `.json` y `.csv`).

### 3. El puerto 8000 está ocupado
*   **Error**: `[Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)`
*   **Solución**: Ejecuta la aplicación en otro puerto:
    ```bash
    uvicorn main:app --port 8001
    ```

### 4. Problemas de codificación (UnicodeDecodeError)
*   **Causa**: Algunos sistemas pueden tener problemas con la codificación de caracteres en los archivos de datos.
*   **Solución**: Verifica que los archivos estén en UTF-8. En `main.py`, se puede forzar la codificación al abrir el archivo: `open('steam_games.json', encoding='utf-8')`.
