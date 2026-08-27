from app.presentation.api.routes.auth import router as auth_router
from app.presentation.api.routes.cart import router as cart_router
from app.presentation.api.routes.catalog import router as catalog_router
from app.presentation.api.routes.checkout import router as checkout_router
from app.presentation.api.routes.cities import router as cities_router
from app.presentation.api.routes.database import router as database_router
from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes.orders import router as orders_router
from app.presentation.api.routes.payments import router as payments_router

__all__ = [
    "auth_router",
    "cart_router",
    "catalog_router",
    "checkout_router",
    "cities_router",
    "database_router",
    "health_router",
    "orders_router",
    "payments_router",
]
