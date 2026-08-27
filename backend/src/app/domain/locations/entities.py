from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.value_objects import Coordinates


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
    coordinates: Coordinates
    is_active: bool = True
