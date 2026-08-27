from uuid import UUID

from app.application.common import UnitOfWork
from app.domain.orders.entities import Order, OrderItem
from app.domain.shared.exceptions import EntityNotFoundError


class OrderService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_order(self, order_id: UUID) -> Order:
        async with self._uow:
            order = await self._uow.orders.get(order_id)
            if order is None:
                raise EntityNotFoundError(f"Order {order_id} not found")
            return order

    async def list_user_orders(self, user_id: UUID) -> list[Order]:
        async with self._uow:
            return await self._uow.orders.list_by_user(user_id)

    async def create_order(self, order: Order, items: list[OrderItem]) -> None:
        async with self._uow:
            await self._uow.orders.add(order)
            for item in items:
                await self._uow.order_items.add(item)
            await self._uow.commit()

    async def add_order_item(self, item: OrderItem) -> None:
        async with self._uow:
            await self._uow.order_items.add(item)
            await self._uow.commit()
