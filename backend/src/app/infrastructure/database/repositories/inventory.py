from sqlalchemy import select

from app.infrastructure.database.models.inventory import InventoryUnitModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class InventoryRepository(SQLAlchemyRepository[InventoryUnitModel]):
    def __init__(self, session):
        super().__init__(session, InventoryUnitModel)

    async def list_available(self, product_id) -> list[InventoryUnitModel]:
        result = await self.session.execute(
            select(InventoryUnitModel)
            .where(InventoryUnitModel.product_id == product_id)
            .where(InventoryUnitModel.is_available.is_(True))
        )
        return list(result.scalars().all())
