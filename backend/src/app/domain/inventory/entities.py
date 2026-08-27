from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class InventoryUnit:
    id: UUID
    product_id: UUID
    city_id: UUID
    latitude: float | None = None
    longitude: float | None = None
    is_available: bool = True
