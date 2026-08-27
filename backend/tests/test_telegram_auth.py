"""
Tests for the authentication API endpoints.

Covers:
1. GET /auth/me with a valid user_id returns 200 and user data.
2. GET /auth/me with an unknown user_id returns 404.
3. POST /auth/register creates a new user and returns 200.
4. POST /auth/register with an existing telegram_id returns 400.
5. POST /auth/telegram with valid initData creates a user and returns 200.
6. POST /auth/telegram with tampered hash returns 401.
7. POST /auth/telegram with empty initData returns 401.
8. POST /auth/telegram with expired auth_date returns 401.
9. POST /auth/telegram updates existing user on subsequent logins.
"""

import time
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.infrastructure.database.models import UserModel
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.telegram.validator import compute_hmac_hash
from app.presentation.api import create_app

TEST_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRsTUVwxYZ1234567890"


def _build_init_data(fields: dict[str, str], bot_token: str = TEST_BOT_TOKEN) -> str:
    _bot_id, bot_secret = bot_token.split(":", 1)
    params = dict(fields)
    params.pop("hash", None)
    sorted_keys = sorted(params.keys(), key=lambda k: k.encode("utf-8"))
    data_check_string = "\n".join(f"{k}={params[k]}" for k in sorted_keys)
    params["hash"] = compute_hmac_hash(data_check_string, bot_secret)
    return "&".join(f"{k}={v}" for k, v in params.items())


def _valid_init_data() -> str:
    return _build_init_data(
        {
            "id": "123456789",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "auth_date": str(int(time.time())),
        }
    )


@pytest.mark.asyncio
async def test_auth_me_returns_user() -> None:
    user_id = uuid4()
    async with SessionFactory() as session:
        user = UserModel(
            telegram_id=111222333,
            username="alice",
            is_admin=False,
            is_active=True,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        user_id = user.id

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get("/auth/me", params={"user_id": str(user_id)})

    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == 111222333
    assert body["username"] == "alice"
    assert body["is_active"] is True


@pytest.mark.asyncio
async def test_auth_me_not_found() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.get(
            "/auth/me",
            params={"user_id": "00000000-0000-0000-0000-000000000000"},
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_auth_register_creates_user() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/register",
            params={"telegram_id": 444555666, "username": "bob"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["telegram_id"] == 444555666
    assert body["username"] == "bob"


@pytest.mark.asyncio
async def test_auth_register_duplicate_telegram_id() -> None:
    async with SessionFactory() as session:
        user = UserModel(
            telegram_id=777888999,
            username="existing",
            is_admin=False,
            is_active=True,
        )
        session.add(user)
        await session.commit()

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/register",
            params={"telegram_id": 777888999, "username": "duplicate"},
        )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_telegram_auth_creates_new_user(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid initData should create a new user and return 200."""
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": _valid_init_data()},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["telegram_id"] == 123456789
    assert body["user"]["username"] == "testuser"
    assert body["user"]["first_name"] == "Test"
    assert body["user"]["last_name"] == "User"
    assert body["user"]["is_active"] is True


@pytest.mark.asyncio
async def test_telegram_auth_rejects_tampered_hash(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tampering with the hash must result in 401."""
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)
    tampered = _valid_init_data().replace("hash=", "hash=x")
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": tampered},
        )

    assert response.status_code == 401
    assert "hash verification failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_telegram_auth_rejects_empty_init_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": ""},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_telegram_auth_rejects_expired_auth_date(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)
    old_auth_date = str(int(time.time()) - 25 * 3600)
    expired_init_data = _build_init_data(
        {
            "id": "123456789",
            "first_name": "Test",
            "auth_date": old_auth_date,
        }
    )
    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": expired_init_data},
        )

    assert response.status_code == 401
    assert "too old" in response.json()["detail"]


@pytest.mark.asyncio
async def test_telegram_auth_updates_existing_user(monkeypatch: pytest.MonkeyPatch) -> None:
    """Subsequent logins should update mutable profile fields."""
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)
    init_data_v1 = _build_init_data(
        {
            "id": "999888777",
            "first_name": "OldName",
            "last_name": "",
            "username": "oldname",
            "auth_date": str(int(time.time())),
        }
    )
    init_data_v2 = _build_init_data(
        {
            "id": "999888777",
            "first_name": "NewName",
            "last_name": "NewLast",
            "username": "newname",
            "auth_date": str(int(time.time())),
        }
    )

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        r1 = await client.post(
            "/auth/telegram",
            json={"init_data": init_data_v1},
        )
        assert r1.status_code == 200
        assert r1.json()["user"]["first_name"] == "OldName"

        r2 = await client.post(
            "/auth/telegram",
            json={"init_data": init_data_v2},
        )
        assert r2.status_code == 200
        assert r2.json()["user"]["first_name"] == "NewName"
        assert r2.json()["user"]["last_name"] == "NewLast"


@pytest.mark.asyncio
async def test_telegram_auth_rejects_wrong_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", TEST_BOT_TOKEN)
    wrong_token = "999999999:WrongSecretKey1234567890ab"
    _bot_id, bot_secret = wrong_token.split(":", 1)
    params = {
        "id": "123456789",
        "first_name": "Test",
        "auth_date": str(int(time.time())),
    }
    sorted_keys = sorted(params.keys(), key=lambda k: k.encode("utf-8"))
    dcs = "\n".join(f"{k}={params[k]}" for k in sorted_keys)
    params["hash"] = compute_hmac_hash(dcs, bot_secret)
    wrong_init_data = "&".join(f"{k}={v}" for k, v in params.items())

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": wrong_init_data},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_telegram_auth_without_bot_token_returns_500(monkeypatch: pytest.MonkeyPatch) -> None:
    """If TELEGRAM_BOT_TOKEN is not configured, return 500."""
    monkeypatch.setattr("app.config.settings.settings.telegram_bot_token", "")

    async with AsyncClient(
        transport=ASGITransport(app=create_app()),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/auth/telegram",
            json={"init_data": _valid_init_data()},
        )

    assert response.status_code == 500

