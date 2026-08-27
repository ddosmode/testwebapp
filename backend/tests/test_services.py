import pytest
from decimal import Decimal
from uuid import uuid4

from app.application.catalog.services import CatalogService
from app.application.inventory.services import InventoryService
from app.application.locations.services import LocationService
from app.application.payments.services import PaymentMethodService
from app.application.settings.services import SettingsService
from app.domain.catalog.entities import Category, Product
from app.domain.inventory.entities import InventoryUnit
from app.domain.locations.entities import City, Location
from app.domain.payments.entities import PaymentMethod
from app.domain.shared.exceptions import EntityNotFoundError
from app.domain.shared.value_objects import Coordinates
from app.domain.settings.entities import Setting


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.categories = FakeCategoryRepo()
        self.products = FakeProductRepo()
        self.inventory = FakeInventoryRepo()
        self.cities = FakeCityRepo()
        self.locations = FakeLocationRepo()
        self.payment_methods = FakePaymentRepo()
        self.settings = FakeSettingsRepo()

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(self, *args: object) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass


class FakeCategoryRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, Category] = {}

    async def get(self, category_id: uuid4) -> Category | None:
        return self._items.get(category_id)

    async def list_active(self) -> list[Category]:
        return [c for c in self._items.values() if c.is_active]

    async def add(self, category: Category) -> None:
        self._items[category.id] = category

    async def remove(self, category_id: uuid4) -> None:
        self._items.pop(category_id, None)


class FakeProductRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, Product] = {}

    async def get(self, product_id: uuid4) -> Product | None:
        return self._items.get(product_id)

    async def list_active(self) -> list[Product]:
        return [p for p in self._items.values() if p.is_active]

    async def add(self, product: Product) -> None:
        self._items[product.id] = product

    async def remove(self, product_id: uuid4) -> None:
        self._items.pop(product_id, None)


class FakeInventoryRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, InventoryUnit] = {}

    async def get(self, unit_id: uuid4) -> InventoryUnit | None:
        return self._items.get(unit_id)

    async def list_available(self, product_id: uuid4) -> list[InventoryUnit]:
        return [u for u in self._items.values() if u.product_id == product_id and u.is_available]

    async def add(self, unit: InventoryUnit) -> None:
        self._items[unit.id] = unit

    async def remove(self, unit_id: uuid4) -> None:
        self._items.pop(unit_id, None)


class FakeCityRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, City] = {}

    async def get(self, city_id: uuid4) -> City | None:
        return self._items.get(city_id)

    async def list_active(self) -> list[City]:
        return [c for c in self._items.values() if c.is_active]

    async def add(self, city: City) -> None:
        self._items[city.id] = city

    async def remove(self, city_id: uuid4) -> None:
        self._items.pop(city_id, None)


class FakeLocationRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, Location] = {}

    async def get(self, location_id: uuid4) -> Location | None:
        return self._items.get(location_id)

    async def list_by_city(self, city_id: uuid4) -> list[Location]:
        return [l for l in self._items.values() if l.city_id == city_id]

    async def add(self, location: Location) -> None:
        self._items[location.id] = location

    async def remove(self, location_id: uuid4) -> None:
        self._items.pop(location_id, None)


class FakePaymentRepo:
    def __init__(self) -> None:
        self._items: dict[uuid4, PaymentMethod] = {}

    async def get(self, payment_id: uuid4) -> PaymentMethod | None:
        return self._items.get(payment_id)

    async def list_active(self) -> list[PaymentMethod]:
        return [p for p in self._items.values() if p.is_active]

    async def add(self, method: PaymentMethod) -> None:
        self._items[method.id] = method

    async def remove(self, payment_id: uuid4) -> None:
        self._items.pop(payment_id, None)


class FakeSettingsRepo:
    def __init__(self) -> None:
        self._items: dict[str, Setting] = {}

    async def get(self, setting_id: uuid4) -> Setting | None:
        for s in self._items.values():
            if s.id == setting_id:
                return s
        return None

    async def get_by_key(self, key: str) -> Setting | None:
        return self._items.get(key)

    async def list_active(self) -> list[Setting]:
        return list(self._items.values())

    async def set(self, setting: Setting) -> None:
        self._items[setting.key] = setting

    async def remove(self, setting_id: uuid4) -> None:
        for key, s in list(self._items.items()):
            if s.id == setting_id:
                del self._items[key]
                break


class TestCatalogService:
    @pytest.fixture
    def service(self) -> CatalogService:
        return CatalogService(FakeUnitOfWork())

    @pytest.mark.asyncio
    async def test_list_products_empty(self, service: CatalogService) -> None:
        products = await service.list_products()
        assert products == []

    @pytest.mark.asyncio
    async def test_create_and_get_product(self, service: CatalogService) -> None:
        product = Product(
            id=uuid4(),
            category_id=uuid4(),
            name="Phone",
            description="Smartphone",
            price=Decimal("699.00"),
        )
        await service.create_product(product)
        fetched = await service.get_product(product.id)
        assert fetched.id == product.id
        assert fetched.name == "Phone"

    @pytest.mark.asyncio
    async def test_get_product_not_found(self, service: CatalogService) -> None:
        with pytest.raises(EntityNotFoundError):
            await service.get_product(uuid4())

    @pytest.mark.asyncio
    async def test_create_category(self, service: CatalogService) -> None:
        category = Category(id=uuid4(), name="Books", slug="books")
        await service.create_category(category)
        assert category.is_active is True


class TestInventoryService:
    @pytest.fixture
    def service(self) -> InventoryService:
        return InventoryService(FakeUnitOfWork())

    @pytest.mark.asyncio
    async def test_create_inventory_unit(self, service: InventoryService) -> None:
        unit = InventoryUnit(id=uuid4(), product_id=uuid4(), city_id=uuid4())
        await service.create_unit(unit)
        assert unit.is_available is True


class TestLocationService:
    @pytest.fixture
    def service(self) -> LocationService:
        return LocationService(FakeUnitOfWork())

    @pytest.mark.asyncio
    async def test_create_city(self, service: LocationService) -> None:
        city = City(id=uuid4(), name="Paris")
        await service.create_city(city)
        assert city.is_active is True

    @pytest.mark.asyncio
    async def test_create_location(self, service: LocationService) -> None:
        location = Location(
            id=uuid4(),
            city_id=uuid4(),
            name="Main Store",
            latitude=48.8566,
            longitude=2.3522,
        )
        await service.create_location(location)
        assert location.name == "Main Store"


class TestPaymentMethodService:
    @pytest.fixture
    def service(self) -> PaymentMethodService:
        return PaymentMethodService(FakeUnitOfWork())

    @pytest.mark.asyncio
    async def test_create_payment_method(self, service: PaymentMethodService) -> None:
        method = PaymentMethod(id=uuid4(), name="PayPal", code="paypal")
        await service.create_method(method)
        assert method.is_active is True


class TestSettingsService:
    @pytest.fixture
    def service(self) -> SettingsService:
        return SettingsService(FakeUnitOfWork())

    @pytest.mark.asyncio
    async def test_set_setting(self, service: SettingsService) -> None:
        setting = Setting(id=uuid4(), key="theme", value="dark")
        await service.set(setting)
        assert setting.key == "theme"
        assert setting.value == "dark"
