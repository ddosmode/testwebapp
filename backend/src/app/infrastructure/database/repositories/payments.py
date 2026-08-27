from app.infrastructure.database.models.payments import PaymentMethodModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class PaymentMethodRepository(SQLAlchemyRepository[PaymentMethodModel]):
    def __init__(self, session):
        super().__init__(session, PaymentMethodModel)
