import pytest
from httpx import ASGITransport, AsyncClient

from app.presentation.api import create_app


@pytest.mark.asyncio
async def test_health() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_database() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/database")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "tables" in body


@pytest.mark.asyncio
async def test_list_products_empty() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/catalog/products")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_categories_empty() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/catalog/categories")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_product_not_found() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/catalog/products/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_product_with_data() -> None:
    from uuid import uuid4
    from decimal import Decimal
    from app.infrastructure.database.session import SessionFactory
    from app.infrastructure.database.models import CategoryModel, ProductModel

    async with SessionFactory() as session:
        category = CategoryModel(name="Test Category", slug="test-category")
        session.add(category)
        await session.flush()

        product = ProductModel(
            category_id=category.id,
            name="Test Product",
            description="A test product",
            price=Decimal("9.99"),
            is_active=True,
        )
        session.add(product)
        await session.commit()

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get(f"/catalog/products/{product.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == str(product.id)
    assert body["name"] == "Test Product"
    assert body["price"] == "9.99"


@pytest.mark.asyncio
async def test_auth_me_not_found() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/auth/me", params={"user_id": "00000000-0000-0000-0000-000000000000"})

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_auth_register() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/register",
            params={"telegram_id": 123456789, "username": "newuser"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == 123456789
    assert body["username"] == "newuser"
