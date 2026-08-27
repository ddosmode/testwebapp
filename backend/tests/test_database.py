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


@pytest.mark.asyncio
async def test_category_crud() -> None:
    from uuid import uuid4
    from app.infrastructure.database.models import CategoryModel

    async with SessionFactory() as session:
        category = CategoryModel(name="Electronics", slug="electronics")
        session.add(category)
        await session.commit()
        await session.refresh(category)

        fetched = await session.get(CategoryModel, category.id)
        assert fetched is not None
        assert fetched.name == "Electronics"
        assert fetched.slug == "electronics"
        assert fetched.is_active is True

        fetched.name = "Updated Electronics"
        await session.commit()
        await session.refresh(fetched)
        assert fetched.name == "Updated Electronics"

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(CategoryModel, category.id)
        assert deleted is None


@pytest.mark.asyncio
async def test_product_crud() -> None:
    from decimal import Decimal
    from app.infrastructure.database.models import CategoryModel, ProductModel

    async with SessionFactory() as session:
        category = CategoryModel(name="Books", slug="books")
        session.add(category)
        await session.flush()

        product = ProductModel(
            category_id=category.id,
            name="Test Book",
            description="A test book",
            price=Decimal("19.99"),
            is_active=True,
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)

        fetched = await session.get(ProductModel, product.id)
        assert fetched is not None
        assert fetched.name == "Test Book"
        assert fetched.price == Decimal("19.99")
        assert fetched.is_active is True

        fetched.name = "Updated Book"
        await session.commit()
        await session.refresh(fetched)
        assert fetched.name == "Updated Book"

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(ProductModel, product.id)
        assert deleted is None


@pytest.mark.asyncio
async def test_user_crud() -> None:
    from app.infrastructure.database.models import UserModel

    async with SessionFactory() as session:
        user = UserModel(
            telegram_id=123456789,
            username="testuser",
            is_admin=False,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        fetched = await session.get(UserModel, user.id)
        assert fetched is not None
        assert fetched.telegram_id == 123456789
        assert fetched.username == "testuser"
        assert fetched.is_active is True

        fetched.username = "updateduser"
        await session.commit()
        await session.refresh(fetched)
        assert fetched.username == "updateduser"

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(UserModel, user.id)
        assert deleted is None


@pytest.mark.asyncio
async def test_inventory_crud() -> None:
    from uuid import uuid4
    from decimal import Decimal
    from app.infrastructure.database.models import CategoryModel, ProductModel, InventoryUnitModel, CityModel

    async with SessionFactory() as session:
        city = CityModel(name="Berlin", is_active=True)
        session.add(city)
        await session.flush()

        category = CategoryModel(name="Toys", slug="toys")
        session.add(category)
        await session.flush()

        product = ProductModel(
            category_id=category.id,
            name="Toy Car",
            description="A toy car",
            price=Decimal("5.99"),
            is_active=True,
        )
        session.add(product)
        await session.flush()

        unit = InventoryUnitModel(
            product_id=product.id,
            city_id=city.id,
            is_available=True,
        )
        session.add(unit)
        await session.commit()
        await session.refresh(unit)

        fetched = await session.get(InventoryUnitModel, unit.id)
        assert fetched is not None
        assert fetched.product_id == product.id
        assert fetched.city_id == city.id
        assert fetched.is_available is True

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(InventoryUnitModel, unit.id)
        assert deleted is None


@pytest.mark.asyncio
async def test_setting_crud() -> None:
    from app.infrastructure.database.models import SettingModel

    async with SessionFactory() as session:
        setting = SettingModel(key="app_name", value="TestApp")
        session.add(setting)
        await session.commit()
        await session.refresh(setting)

        fetched = await session.get(SettingModel, setting.id)
        assert fetched is not None
        assert fetched.key == "app_name"
        assert fetched.value == "TestApp"

        fetched.value = "UpdatedApp"
        await session.commit()
        await session.refresh(fetched)
        assert fetched.value == "UpdatedApp"

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(SettingModel, setting.id)
        assert deleted is None


@pytest.mark.asyncio
async def test_order_crud() -> None:
    from uuid import uuid4
    from decimal import Decimal
    from app.infrastructure.database.models import UserModel, OrderModel

    async with SessionFactory() as session:
        user = UserModel(
            telegram_id=987654321,
            username="orderuser",
            is_admin=False,
            is_active=True,
        )
        session.add(user)
        await session.flush()

        order = OrderModel(
            user_id=user.id,
            total=Decimal("49.99"),
            status="created",
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)

        fetched = await session.get(OrderModel, order.id)
        assert fetched is not None
        assert fetched.user_id == user.id
        assert fetched.total == Decimal("49.99")
        assert fetched.status == "created"

        fetched.status = "paid"
        await session.commit()
        await session.refresh(fetched)
        assert fetched.status == "paid"

        await session.delete(fetched)
        await session.commit()

        deleted = await session.get(OrderModel, order.id)
        assert deleted is None
