from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str = "EUR"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")


@dataclass(frozen=True, slots=True)
class Coordinates:
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")


@dataclass(frozen=True, slots=True)
class TelegramUserId:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("Telegram user ID must be positive")


@dataclass(frozen=True, slots=True)
class EntityId:
    value: UUID
