from dataclasses import dataclass
from uuid import UUID

from app.domain.shared.value_objects import Coordinates


@dataclass(frozen=True, slots=True)
class InventoryUnit:
    id: UUID
    product_id: UUID
    city_id: UUID
    coordinates: Coordinates | None = None
    is_available: bool = True
