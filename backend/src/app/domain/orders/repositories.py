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


class OrderItemRepository(ABC):
    @abstractmethod
    async def get(self, item_id: UUID) -> OrderItem | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_order(self, order_id: UUID) -> list[OrderItem]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, item: OrderItem) -> None:
        raise NotImplementedError
