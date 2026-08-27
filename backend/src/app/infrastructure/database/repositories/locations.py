from sqlalchemy import select

from app.infrastructure.database.models.locations import CityModel, LocationModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository[CityModel]):
    def __init__(self, session):
        super().__init__(session, CityModel)

    async def list_active(self) -> list[CityModel]:
        result = await self.session.execute(
            select(CityModel)
            .where(CityModel.is_active.is_(True))
            .order_by(CityModel.name)
        )
        return list(result.scalars().all())


class LocationRepository(SQLAlchemyRepository[LocationModel]):
    def __init__(self, session):
        super().__init__(session, LocationModel)

    async def list_by_city(self, city_id) -> list[LocationModel]:
        result = await self.session.execute(
            select(LocationModel)
            .where(LocationModel.city_id == city_id)
            .where(LocationModel.is_active.is_(True))
            .order_by(LocationModel.name)
        )
        return list(result.scalars().all())
