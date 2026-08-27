from app.infrastructure.database.models.inventory import InventoryUnitModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class InventoryRepository(SQLAlchemyRepository[InventoryUnitModel]):
    def __init__(self, session):
        super().__init__(session, InventoryUnitModel)
