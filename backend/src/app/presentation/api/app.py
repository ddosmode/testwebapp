from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database import Base
from app.infrastructure.database.session import engine
from app.presentation.api.routes import (
    auth_router,
    cart_router,
    catalog_router,
    checkout_router,
    cities_router,
    database_router,
    health_router,
    orders_router,
    payments_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="TestWebApp API",
        version="1.0.0",
        lifespan=lifespan,
    )

    application.include_router(health_router)
    application.include_router(database_router)
    application.include_router(catalog_router)
    application.include_router(cities_router)
    application.include_router(payments_router)
    application.include_router(cart_router)
    application.include_router(checkout_router)
    application.include_router(orders_router)
    application.include_router(auth_router)

    application.add_api_route(
        "/health/database",
        lambda: {"status": "ok"},
        methods=["GET"],
        tags=["health"],
    )

    return application


app = create_app()
