from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class City:
    id: UUID
    name: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class Location:
    id: UUID
    city_id: UUID
    name: str
    latitude: float
    longitude: float
    is_active: bool = True
