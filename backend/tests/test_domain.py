from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.catalog.entities import Category, Product
from app.domain.inventory.entities import InventoryUnit
from app.domain.locations.entities import City, Location
from app.domain.orders.entities import Order, OrderItem, OrderStatus
from app.domain.payments.entities import PaymentMethod
from app.domain.settings.entities import Setting
from app.domain.shared.exceptions import BusinessRuleViolation, EntityNotFoundError
from app.domain.shared.value_objects import Coordinates, Money, TelegramUserId
from app.domain.users.entities import User


class TestCategory:
    def test_create_category(self) -> None:
        category = Category(id=uuid4(), name="Electronics", slug="electronics")
        assert category.id is not None
        assert category.name == "Electronics"
        assert category.slug == "electronics"
        assert category.is_active is True

    def test_create_inactive_category(self) -> None:
        category = Category(id=uuid4(), name="Old", slug="old", is_active=False)
        assert category.is_active is False


class TestProduct:
    def test_create_product(self) -> None:
        product = Product(
            id=uuid4(),
            category_id=uuid4(),
            name="Laptop",
            description="A laptop",
            price=Decimal("999.99"),
        )
        assert product.name == "Laptop"
        assert product.price == Decimal("999.99")
        assert product.is_active is True

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            Product(
                id=uuid4(),
                category_id=uuid4(),
                name="   ",
                description="desc",
                price=Decimal("10.00"),
            )

    def test_negative_price_raises(self) -> None:
        with pytest.raises(ValueError, match="Product price cannot be negative"):
            Product(
                id=uuid4(),
                category_id=uuid4(),
                name="Item",
                description="desc",
                price=Decimal("-1.00"),
            )


class TestInventoryUnit:
    def test_create_inventory_unit(self) -> None:
        unit = InventoryUnit(id=uuid4(), product_id=uuid4(), city_id=uuid4())
        assert unit.is_available is True

    def test_create_unavailable_unit(self) -> None:
        unit = InventoryUnit(
            id=uuid4(),
            product_id=uuid4(),
            city_id=uuid4(),
            is_available=False,
        )
        assert unit.is_available is False


class TestCity:
    def test_create_city(self) -> None:
        city = City(id=uuid4(), name="Berlin")
        assert city.name == "Berlin"
        assert city.is_active is True


class TestLocation:
    def test_create_location(self) -> None:
        location = Location(
            id=uuid4(),
            city_id=uuid4(),
            name="Main Store",
            latitude=52.52,
            longitude=13.405,
        )
        assert location.name == "Main Store"
        assert location.latitude == 52.52


class TestCoordinates:
    def test_valid_coordinates(self) -> None:
        c = Coordinates(latitude=0.0, longitude=0.0)
        assert c.latitude == 0.0
        assert c.longitude == 0.0

    def test_invalid_latitude_raises(self) -> None:
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            Coordinates(latitude=100.0, longitude=0.0)

    def test_invalid_longitude_raises(self) -> None:
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            Coordinates(latitude=0.0, longitude=200.0)


class TestMoney:
    def test_valid_money(self) -> None:
        m = Money(amount=Decimal("100.00"))
        assert m.amount == Decimal("100.00")
        assert m.currency == "EUR"

    def test_negative_amount_raises(self) -> None:
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money(amount=Decimal("-1.00"))

    def test_invalid_currency_raises(self) -> None:
        with pytest.raises(ValueError, match="Currency must be a 3-letter ISO code"):
            Money(amount=Decimal("10.00"), currency="EURO")


class TestTelegramUserId:
    def test_valid_id(self) -> None:
        uid = TelegramUserId(value=12345)
        assert uid.value == 12345

    def test_invalid_id_raises(self) -> None:
        with pytest.raises(ValueError, match="Telegram user ID must be positive"):
            TelegramUserId(value=0)


class TestUser:
    def test_create_user(self) -> None:
        user = User(id=uuid4(), telegram_id=12345, username="alice")
        assert user.telegram_id == 12345
        assert user.username == "alice"
        assert user.is_admin is False
        assert user.is_active is True


class TestOrder:
    def test_create_order(self) -> None:
        order = Order(
            id=uuid4(),
            user_id=uuid4(),
            total=Decimal("50.00"),
            currency="EUR",
        )
        assert order.total == Decimal("50.00")
        assert order.status == OrderStatus.CREATED

    def test_order_item(self) -> None:
        item = OrderItem(
            id=uuid4(),
            order_id=uuid4(),
            product_id=uuid4(),
            quantity=2,
            unit_price=Decimal("10.00"),
        )
        assert item.quantity == 2
        assert item.unit_price == Decimal("10.00")


class TestOrderStatus:
    def test_status_values(self) -> None:
        assert OrderStatus.CREATED.value == "created"
        assert OrderStatus.PAID.value == "paid"
        assert OrderStatus.PROCESSING.value == "processing"
        assert OrderStatus.COMPLETED.value == "completed"
        assert OrderStatus.CANCELLED.value == "cancelled"


class TestPaymentMethod:
    def test_create_payment_method(self) -> None:
        pm = PaymentMethod(id=uuid4(), name="Credit Card", code="cc")
        assert pm.name == "Credit Card"
        assert pm.code == "cc"
        assert pm.is_active is True


class TestSetting:
    def test_create_setting(self) -> None:
        setting = Setting(id=uuid4(), key="theme", value="dark")
        assert setting.key == "theme"
        assert setting.value == "dark"


class TestExceptions:
    def test_entity_not_found_error(self) -> None:
        with pytest.raises(EntityNotFoundError):
            raise EntityNotFoundError("missing")

    def test_business_rule_violation(self) -> None:
        with pytest.raises(BusinessRuleViolation):
            raise BusinessRuleViolation("rule broken")

    def test_domain_error_is_exception(self) -> None:
        with pytest.raises(Exception):
            raise EntityNotFoundError("base is Exception")
