from fastapi import FastAPI

from app.presentation.api.routes import database_router, health_router


def create_app() -> FastAPI:
    application = FastAPI(
        title="TestWebApp API",
        version="0.1.0",
    )

    application.include_router(health_router)
    application.include_router(database_router)

    return application


app = create_app()
