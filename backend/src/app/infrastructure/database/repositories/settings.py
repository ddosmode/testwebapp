from sqlalchemy import select

from app.infrastructure.database.models.settings import SettingModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class SettingsRepository(SQLAlchemyRepository[SettingModel]):
    def __init__(self, session):
        super().__init__(session, SettingModel)

    async def get_by_key(self, key: str) -> SettingModel | None:
        result = await self.session.execute(
            select(SettingModel).where(SettingModel.key == key)
        )
        return result.scalar_one_or_none()
