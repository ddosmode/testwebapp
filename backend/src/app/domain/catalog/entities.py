from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Category:
    id: UUID
    name: str
    slug: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class Product:
    id: UUID
    category_id: UUID
    name: str
    description: str
    price: Decimal
    currency: str = "EUR"
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
