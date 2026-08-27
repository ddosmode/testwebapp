from sqlalchemy import select

from app.infrastructure.database.models.orders import OrderItemModel, OrderModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository[OrderModel]):
    def __init__(self, session):
        super().__init__(session, OrderModel)

    async def list_by_user(self, user_id) -> list[OrderModel]:
        result = await self.session.execute(
            select(OrderModel)
            .where(OrderModel.user_id == user_id)
            .order_by(OrderModel.created_at.desc())
        )
        return list(result.scalars().all())


class OrderItemRepository(SQLAlchemyRepository[OrderItemModel]):
    def __init__(self, session):
        super().__init__(session, OrderItemModel)

    async def list_by_order(self, order_id) -> list[OrderItemModel]:
        result = await self.session.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        return list(result.scalars().all())
