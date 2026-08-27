from uuid import UUID

from app.application.common import UnitOfWork
from app.domain.catalog.entities import Category, Product
from app.domain.shared.exceptions import EntityNotFoundError


class CatalogService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def list_products(self) -> list[Product]:
        async with self._uow:
            return await self._uow.products.list_active()

    async def get_product(self, product_id: UUID) -> Product:
        async with self._uow:
            product = await self._uow.products.get(product_id)
            if product is None:
                raise EntityNotFoundError(f"Product {product_id} not found")
            return product

    async def create_product(self, product: Product) -> None:
        async with self._uow:
            await self._uow.products.add(product)
            await self._uow.commit()

    async def create_category(self, category: Category) -> None:
        async with self._uow:
            await self._uow.categories.add(category)
            await self._uow.commit()
