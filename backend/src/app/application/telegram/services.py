"""
Telegram authentication application service.

Responsibilities:
- Validate Telegram WebApp initData cryptographically.
- Create a new user from Telegram identity data or update an existing one.
- Return the authenticated user domain entity.

Security contract:
- All user identity fields MUST originate from the verified initData payload.
- The ``initDataUnsafe`` object MUST NEVER be used here.
- Only fields present in the verified payload are applied to the user entity.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from app.domain.shared.exceptions import TelegramAuthError, TelegramInitDataError
from app.domain.users.entities import User
from app.domain.users.repositories import UserRepository
from app.infrastructure.telegram.validator import (
    TelegramInitDataError as ValidatorInitDataError,
)
from app.infrastructure.telegram.validator import verify_init_data


class TelegramAuthService:
    """
    Service that handles Telegram WebApp authentication.

    Uses the verified initData payload to identify or create a local user
    record. Each successful authentication refreshes the user's profile
    data from Telegram.
    """

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    async def authenticate(self, init_data: str) -> User:
        """
        Authenticate a user via Telegram WebApp initData.

        Args:
            init_data: Raw query string from the Telegram WebApp client.

        Returns:
            The authenticated :class:`User` domain entity.

        Raises:
            TelegramInitDataError: If the initData fails cryptographic
                verification or contains malformed fields.
            TelegramAuthError: If a valid initData references a Telegram
                user ID that is not positive (should not happen after
                validation, but defensive check included).
        """
        try:
            payload = verify_init_data(init_data)
        except ValidatorInitDataError as exc:
            raise TelegramInitDataError(str(exc)) from exc

        telegram_id = payload.get("id")
        if telegram_id is None:
            raise TelegramAuthError("initData does not contain a user 'id'")

        if not isinstance(telegram_id, int) or telegram_id <= 0:
            raise TelegramAuthError(
                f"Telegram user ID must be a positive integer, got {telegram_id!r}"
            )

        user = await self._user_repository.get_by_telegram_id(telegram_id)

        if user is None:
            user = await self._create_user_from_payload(telegram_id, payload)
        else:
            user = await self._update_user_from_payload(user, payload)

        return user

    async def _create_user_from_payload(
        self, telegram_id: int, payload: dict[str, Any]
    ) -> User:
        """Create a new local user from verified Telegram payload."""
        now = datetime.utcnow()

        user = User(
            id=UUID(int=0),  # placeholder; replaced by DB-generated UUID
            telegram_id=telegram_id,
            username=_first_str(payload.get("username")),
            first_name=_first_str(payload.get("first_name")),
            last_name=_first_str(payload.get("last_name")),
            photo_url=_first_str(payload.get("photo_url")),
            created_at=now,
            updated_at=now,
        )

        # Persist via repository; the repository/ORM will assign the real UUID.
        await self._user_repository.add(user)
        return user

    async def _update_user_from_payload(
        self, user: User, payload: dict[str, Any]
    ) -> User:
        """
        Refresh mutable profile fields from the verified Telegram payload.

        Only updates fields that are present and non-empty in the payload,
        preserving any existing values otherwise.
        """
        updated_user = User(
            id=user.id,
            telegram_id=user.telegram_id,
            username=_first_non_empty(payload.get("username"), user.username),
            first_name=_first_non_empty(payload.get("first_name"), user.first_name),
            last_name=_first_non_empty(payload.get("last_name"), user.last_name),
            photo_url=_first_non_empty(payload.get("photo_url"), user.photo_url),
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=datetime.utcnow(),
        )

        await self._user_repository.update(updated_user)
        return updated_user


def _first_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _first_non_empty(new_value: Any, current: str | None) -> str | None:
    candidate = _first_str(new_value)
    return candidate if candidate is not None else current
