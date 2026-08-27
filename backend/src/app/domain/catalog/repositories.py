from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Category, Product


class CategoryRepository(ABC):
    @abstractmethod
    async def get(self, category_id: UUID) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, category_id: UUID) -> None:
        raise NotImplementedError


class ProductRepository(ABC):
    @abstractmethod
    async def get(self, product_id: UUID) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, product: Product) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, product_id: UUID) -> None:
        raise NotImplementedError
