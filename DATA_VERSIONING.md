# Control de Versiones de Datos (DVC)

Este proyecto utiliza [DVC (Data Version Control)](https://dvc.org/) para gestionar versiones de los datasets grandes y modelos de Machine Learning.

## Archivos Trackeados

*   `steam_games.json`
*   `steam_games.csv`

Estos archivos no se guardan directamente en el repositorio de Git (para evitar problemas de tamaño), sino que se guarda un puntero (`.dvc`) que referencia al archivo real.

## Flujo de Trabajo

### 1. Clonar y Obtener Datos

Al clonar el repositorio, los archivos de datos no estarán presentes físicamente. Para obtenerlos (si están configurados en un almacenamiento remoto):

```bash
git clone <repo>
dvc pull
```

*Nota: Actualmente el almacenamiento remoto no está configurado, por lo que los datos deben colocarse manualmente en local si no se tiene acceso al cache compartido.*

### 2. Actualizar Datos

Si modificas `steam_games.json` o `steam_games.csv`:

```bash
# 1. Agregar cambios a DVC
dvc add steam_games.json steam_games.csv

# 2. Esto actualiza los archivos .dvc. Ahora commitea esos cambios a Git
git add steam_games.json.dvc steam_games.csv.dvc
git commit -m "update: dataset version v2"
```

### 3. Historial y Versiones

Puedes volver a versiones anteriores de los datos igual que con el código:

```bash
git checkout <commit-hash-anterior>
dvc checkout
```

## Beneficios

1.  **Reproducibilidad**: Cada commit de git está enlazado a una versión exacta de los datos.
2.  **Almacenamiento Eficiente**: Git no se sobrecarga con archivos binarios o CSVs gigantes.
3.  **Colaboración**: Permite compartir datasets grandes de manera segura (configurando un remote S3/GDrive/Azure).
