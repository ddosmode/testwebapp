from app.application.common import UnitOfWork
from app.domain.inventory.entities import InventoryUnit


class InventoryService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def create_unit(self, unit: InventoryUnit) -> None:
        async with self._uow:
            await self._uow.inventory.add(unit)
            await self._uow.commit()
