from sqlalchemy import select

from app.infrastructure.database.models.catalog import CategoryModel, ProductModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository[CategoryModel]):
    def __init__(self, session):
        super().__init__(session, CategoryModel)

    async def list_active(self) -> list[ProductModel]:
        result = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.is_active.is_(True))
            .order_by(ProductModel.name)
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> CategoryModel | None:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.slug == slug)
        )
        return result.scalar_one_or_none()


class ProductRepository(SQLAlchemyRepository[ProductModel]):
    def __init__(self, session):
        super().__init__(session, ProductModel)

    async def list_active(self) -> list[ProductModel]:
        result = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.is_active.is_(True))
            .order_by(ProductModel.name)
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> ProductModel | None:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.slug == slug)
        )
        return result.scalar_one_or_none()
