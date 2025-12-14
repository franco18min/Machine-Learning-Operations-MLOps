# Guía de Contribución

¡Gracias por tu interés en contribuir a este proyecto de MLOps! Esta guía establece los estándares y procesos para asegurar la calidad y consistencia del código.

## Estándares de Código

### Python
*   **Estilo**: Seguimos la guía de estilo **PEP 8**.
*   **Indentación**: Usamos **4 espacios** por nivel de indentación (consistente con el código base actual).
*   **Longitud de línea**: Intentamos mantener las líneas debajo de 100 caracteres para mejor legibilidad.
*   **Tipado**: Se recomienda el uso de Type Hints en las definiciones de funciones (ej. `def funcion(param: str) -> dict:`).
*   **Imports**: Organizar los imports en el siguiente orden:
    1.  Librerías estándar (ej. `os`, `sys`).
    2.  Librerías de terceros (ej. `pandas`, `fastapi`).
    3.  Imports locales del proyecto (ej. `from model import prediction`).

### Documentación
*   Todas las funciones públicas deben tener **Docstrings** claros explicando su propósito, parámetros y retorno.

## Proceso de Pull Requests (PR)

1.  **Fork y Branch**:
    *   Haz un fork del repositorio.
    *   Crea una rama (branch) para tu feature o fix: `git checkout -b feature/nueva-funcionalidad`.

2.  **Desarrollo**:
    *   Implementa tus cambios.
    *   Asegúrate de que el código existente siga funcionando.
    *   Si añades una nueva funcionalidad, agrega tests unitarios en la carpeta `tests/`.

3.  **Tests**:
    *   Ejecuta la suite de pruebas antes de enviar tu PR:
        ```bash
        pytest tests/
        ```
    *   Asegúrate de que todos los tests pasen (verde).

4.  **Envío**:
    *   Haz push de tu rama a tu fork.
    *   Abre un Pull Request hacia la rama `main` del repositorio original.
    *   Describe claramente qué cambios has realizado y por qué.

## Convenciones de Commits

Utilizamos **Conventional Commits** para mantener un historial limpio y legible. La estructura básica es:

```
<tipo>: <descripción breve>

[cuerpo opcional]
```

### Tipos Comunes
*   `feat`: Una nueva funcionalidad (ej. `feat: agregar endpoint de recomendaciones`).
*   `fix`: Corrección de un bug (ej. `fix: corregir error de tipo en predicción`).
*   `docs`: Cambios solo en documentación (ej. `docs: actualizar deployment.md`).
*   `style`: Cambios que no afectan el significado del código (espacios, formato, etc.).
*   `refactor`: Cambio de código que no arregla un bug ni añade una funcionalidad.
*   `test`: Añadir o corregir tests (ej. `test: agregar prueba para carga de csv`).
*   `chore`: Tareas de mantenimiento, actualización de dependencias, etc.

### Ejemplo
```
feat: implementar validación de año en endpoint genres

Se agregó una verificación para asegurar que el año ingresado sea numérico antes de procesar.
```
