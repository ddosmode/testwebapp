from app.application.common import UnitOfWork
from app.domain.locations.entities import City, Location


class LocationService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def create_city(self, city: City) -> None:
        async with self._uow:
            await self._uow.cities.add(city)
            await self._uow.commit()

    async def create_location(self, location: Location) -> None:
        async with self._uow:
            await self._uow.locations.add(location)
            await self._uow.commit()
