from abc import ABC, abstractmethod
from uuid import UUID

from .entities import Payment, PaymentMethod


class PaymentMethodRepository(ABC):
    @abstractmethod
    async def get(self, method_id: UUID) -> PaymentMethod | None:
        raise NotImplementedError

    @abstractmethod
    async def list_active(self) -> list[PaymentMethod]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, method: PaymentMethod) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, method_id: UUID) -> None:
        raise NotImplementedError


class PaymentRepository(ABC):
    @abstractmethod
    async def get(self, payment_id: UUID) -> Payment | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, payment: Payment) -> None:
        raise NotImplementedError
