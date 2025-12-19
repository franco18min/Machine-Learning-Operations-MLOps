from fastapi import FastAPI
from src.api.routes import router
from src.utils.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.

    Returns:
        FastAPI: The configured application instance.
    """
    app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)

    app.include_router(router)

    return app


app = create_app()
