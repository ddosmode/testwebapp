from uuid import UUID

from fastapi import FastAPI, HTTPException

from app.infrastructure.database import Base
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork


async def health() -> dict[str, str]:
    return {"status": "ok"}


async def database() -> dict[str, object]:
    return {
        "status": "ok",
        "tables": sorted(Base.metadata.tables.keys()),
    }


async def list_products() -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        products = await uow.products.list_active()

        return [
            {
                "id": str(product.id),
                "category_id": str(product.category_id),
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "is_active": product.is_active,
            }
            for product in products
        ]


async def get_product(product_id: UUID) -> dict[str, object]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        product = await uow.products.get(product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return {
            "id": str(product.id),
            "category_id": str(product.category_id),
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "is_active": product.is_active,
        }


async def list_categories() -> list[dict[str, object]]:
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        categories = await uow.categories.list()

        return [
            {
                "id": str(category.id),
                "name": category.name,
                "is_active": category.is_active,
            }
            for category in categories
        ]


def create_app() -> FastAPI:
    application = FastAPI(
        title="TestWebApp API",
        version="1.0.0",
    )

    application.add_api_route(
        "/health",
        health,
        methods=["GET"],
        tags=["health"],
    )

    application.add_api_route(
        "/database",
        database,
        methods=["GET"],
        tags=["database"],
    )

    application.add_api_route(
        "/health/database",
        health,
        methods=["GET"],
        tags=["health"],
    )

    application.add_api_route(
        "/catalog/products",
        list_products,
        methods=["GET"],
        tags=["catalog"],
    )

    application.add_api_route(
        "/catalog/products/{product_id}",
        get_product,
        methods=["GET"],
        tags=["catalog"],
    )

    application.add_api_route(
        "/catalog/categories",
        list_categories,
        methods=["GET"],
        tags=["catalog"],
    )

    return application


app = create_app()
