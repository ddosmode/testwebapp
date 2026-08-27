from app.infrastructure.database.models.orders import OrderModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository[OrderModel]):
    def __init__(self, session):
        super().__init__(session, OrderModel)
