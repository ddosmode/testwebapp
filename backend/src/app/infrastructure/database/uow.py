from collections.abc import Callable
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.repositories import (
    CategoryRepository,
    CityRepository,
    InventoryRepository,
    LocationRepository,
    OrderItemRepository,
    OrderRepository,
    PaymentMethodRepository,
    PaymentRepository,
    ProductRepository,
    SettingsRepository,
    UserRepository,
)


class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()

        self.categories = CategoryRepository(self.session)
        self.products = ProductRepository(self.session)
        self.inventory = InventoryRepository(self.session)
        self.cities = CityRepository(self.session)
        self.locations = LocationRepository(self.session)
        self.orders = OrderRepository(self.session)
        self.order_items = OrderItemRepository(self.session)
        self.payment_methods = PaymentMethodRepository(self.session)
        self.payments = PaymentRepository(self.session)
        self.settings = SettingsRepository(self.session)
        self.users = UserRepository(self.session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.session is None:
            return

        if exc_type is not None:
            await self.rollback()

        await self.session.close()

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork is not active")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            return
        await self.session.rollback()
