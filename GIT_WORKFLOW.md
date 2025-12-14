# Git Workflow

Este documento describe el flujo de trabajo de Git adoptado por el equipo para mantener un historial limpio y un desarrollo ordenado.

## Estructura de Ramas

*   **`main`**: Rama de producción. Contiene código estable y desplegable. Solo se permiten merges desde `develop` o `hotfix/*`.
*   **`develop`**: Rama principal de desarrollo. Contiene las últimas funcionalidades integradas. Todas las PRs de nuevas características deben apuntar aquí.
*   **`feature/*`**: Ramas para nuevas características. Se crean a partir de `develop` y se fusionan de vuelta a `develop`.
    *   Nomenclatura: `feature/nombre-descriptivo` (ej. `feature/nueva-api-recomendacion`).
*   **`hotfix/*`**: Ramas para correcciones urgentes en producción. Se crean a partir de `main` y se fusionan a `main` y `develop`.
*   **`release/*`**: Ramas para preparar una nueva versión. Se crean desde `develop` y se fusionan a `main` y `develop`.

## Flujo de Trabajo

1.  **Iniciar una Tarea**:
    *   Asegúrate de estar en `develop` y actualizado:
        ```bash
        git checkout develop
        git pull origin develop
        ```
    *   Crea una nueva rama:
        ```bash
        git checkout -b feature/mi-nueva-tarea
        ```

2.  **Desarrollo**:
    *   Realiza tus cambios y commits siguiendo las convenciones.
    *   Ejecuta pruebas localmente antes de hacer push.

3.  **Pull Request (PR)**:
    *   Sube tu rama al repositorio remoto:
        ```bash
        git push origin feature/mi-nueva-tarea
        ```
    *   Abre un Pull Request en GitHub apuntando a `develop`.
    *   Completa la plantilla de PR.

4.  **Revisión y Merge**:
    *   Solicita revisión de código a un compañero.
    *   Una vez aprobado, realiza el merge (preferiblemente `Squash and Merge` para mantener el historial limpio).

## Convenciones de Commits

Seguimos la especificación de [Conventional Commits](https://www.conventionalcommits.org/):

*   `feat`: Nueva característica.
*   `fix`: Corrección de errores.
*   `docs`: Cambios en documentación.
*   `style`: Formato, puntos y comas faltantes, etc. (no afecta la lógica).
*   `refactor`: Refactorización de código.
*   `test`: Añadir o corregir tests.
*   `chore`: Tareas de mantenimiento (build, herramientas, etc.).

Ejemplo:
```
feat: agregar endpoint de predicción de precios
```
