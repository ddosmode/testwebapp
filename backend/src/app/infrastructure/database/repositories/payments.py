from sqlalchemy import select

from app.infrastructure.database.models.payments import PaymentMethodModel, PaymentModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class PaymentMethodRepository(SQLAlchemyRepository[PaymentMethodModel]):
    def __init__(self, session):
        super().__init__(session, PaymentMethodModel)

    async def list_active(self) -> list[PaymentMethodModel]:
        result = await self.session.execute(
            select(PaymentMethodModel)
            .where(PaymentMethodModel.is_active.is_(True))
            .order_by(PaymentMethodModel.name)
        )
        return list(result.scalars().all())


class PaymentRepository(SQLAlchemyRepository[PaymentModel]):
    def __init__(self, session):
        super().__init__(session, PaymentModel)
