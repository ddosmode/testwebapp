import pytest
from sqlalchemy import text
from app.infrastructure.database.session import SessionFactory

from app.infrastructure.database import Base
from app.infrastructure.database.session import engine
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_database_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        assert result.scalar_one() == 1


@pytest.mark.asyncio
async def test_database_schema():
    expected = {
        "categories",
        "products",
        "inventory_units",
        "cities",
        "orders",
        "payment_methods",
        "settings",
        "users",
    }

    assert expected.issubset(Base.metadata.tables.keys())

    for table in Base.metadata.tables.values():
        assert table.primary_key.columns


@pytest.mark.asyncio
async def test_unit_of_work():
    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        assert uow.session is not None
        assert uow.categories is not None
        assert uow.products is not None
        assert uow.inventory is not None
        assert uow.cities is not None
        assert uow.orders is not None
        assert uow.payment_methods is not None
        assert uow.settings is not None
        assert uow.users is not None
