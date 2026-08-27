from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.application.catalog.services import CatalogService
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/catalog", tags=["catalog"])


def get_catalog_service() -> CatalogService:
    return CatalogService(SqlAlchemyUnitOfWork(SessionFactory))


@router.get("/products")
async def list_products() -> list[dict[str, object]]:
    service = get_catalog_service()
    products = await service.list_products()

    return [
        {
            "id": str(product.id),
            "category_id": str(product.category_id),
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "currency": product.currency,
            "is_active": product.is_active,
        }
        for product in products
    ]


@router.get("/products/{product_id}")
async def get_product(product_id: UUID) -> dict[str, object]:
    service = get_catalog_service()

    try:
        product = await service.get_product(product_id)
    except Exception as exc:
        if exc.__class__.__name__ == "EntityNotFoundError":
            raise HTTPException(status_code=404, detail="Product not found") from exc
        raise

    return {
        "id": str(product.id),
        "category_id": str(product.category_id),
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "currency": product.currency,
        "is_active": product.is_active,
    }


@router.get("/categories")
async def list_categories() -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        categories = await uow.categories.list_active()

    return [
        {
            "id": str(category.id),
            "name": category.name,
            "slug": getattr(category, "slug", ""),
            "is_active": category.is_active,
        }
        for category in categories
    ]
