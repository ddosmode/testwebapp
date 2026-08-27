from app.presentation.api.routes.catalog import router as catalog_router
from app.presentation.api.routes.database import router as database_router
from app.presentation.api.routes.health import router as health_router

__all__ = [
    "catalog_router",
    "database_router",
    "health_router",
]
