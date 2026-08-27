from app.application.common import UnitOfWork
from app.domain.payments.entities import PaymentMethod


class PaymentMethodService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def create_method(self, method: PaymentMethod) -> None:
        async with self._uow:
            await self._uow.payment_methods.add(method)
            await self._uow.commit()
