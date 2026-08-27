from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Order, OrderItem


class OrderRepository(ABC):
    @abstractmethod
    async def get(self, order_id: UUID) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, item: OrderItem) -> None:
        raise NotImplementedError
