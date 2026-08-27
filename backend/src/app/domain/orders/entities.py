from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class OrderStatus(StrEnum):
    CREATED = "created"
    PAID = "paid"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class OrderItem:
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    total: Decimal
    currency: str
    status: OrderStatus = OrderStatus.CREATED
