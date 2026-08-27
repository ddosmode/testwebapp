from app.application.common import UnitOfWork
from app.domain.settings.entities import Setting


class SettingsService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def set(self, setting: Setting) -> None:
        async with self._uow:
            await self._uow.settings.set(setting)
            await self._uow.commit()
