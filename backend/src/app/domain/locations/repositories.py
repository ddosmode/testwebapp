from abc import ABC, abstractmethod
from uuid import UUID

from .entities import City, Location


class CityRepository(ABC):
    @abstractmethod
    async def get(self, city_id: UUID) -> City | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[City]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, city: City) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, city_id: UUID) -> None:
        raise NotImplementedError


class LocationRepository(ABC):
    @abstractmethod
    async def get(self, location_id: UUID) -> Location | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_city(self, city_id: UUID) -> list[Location]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, location: Location) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, location_id: UUID) -> None:
        raise NotImplementedError
