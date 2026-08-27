from abc import ABC, abstractmethod
from uuid import UUID

from .entities import InventoryUnit


class InventoryRepository(ABC):
    @abstractmethod
    async def get(self, unit_id: UUID) -> InventoryUnit | None:
        raise NotImplementedError

    @abstractmethod
    async def list_available(self, product_id: UUID) -> list[InventoryUnit]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, unit: InventoryUnit) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, unit_id: UUID) -> None:
        raise NotImplementedError
