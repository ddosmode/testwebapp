from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PaymentMethod:
    id: UUID
    name: str
    code: str
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class Payment:
    id: UUID
    order_id: UUID
    payment_method_id: UUID
    amount: str
    currency: str
    status: str
