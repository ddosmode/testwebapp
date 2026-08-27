"""
Telegram WebApp initData cryptographic validator.

Security model:
- The backend MUST ONLY trust the `initData` string received from the client.
- The `initDataUnsafe` object MUST NEVER be used for authentication — it is
  client-controlled and trivially forgeable.
- This module verifies the HMAC-SHA256 `hash` field inside `initData` using
  the bot token as the secret key, as specified by Telegram.

Reference: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
"""

from __future__ import annotations

import hashlib
import hmac
from collections import OrderedDict
from typing import Any
from urllib.parse import parse_qsl


class TelegramInitDataError(Exception):
    """Raised when Telegram initData fails cryptographic verification."""


def parse_init_data(init_data: str) -> dict[str, str]:
    """
    Parse the raw initData query string into an ordered dictionary.

    The order of parameters matters for hash verification, so we preserve
    the original insertion order from the query string. Duplicate keys are
    not expected but are silently dropped.
    """
    if not init_data or not init_data.strip():
        raise TelegramInitDataError("initData string is empty")

    # parse_qsl preserves order from the query string
    params: dict[str, str] = OrderedDict()
    for key, value in parse_qsl(init_data, keep_blank_values=True):
        params[key] = value

    if "hash" not in params:
        raise TelegramInitDataError("initData missing 'hash' field")

    return params


def compute_data_check_string(params: dict[str, str]) -> str:
    """
    Build the Telegram data-check-string from initData params.

    The `hash` field MUST NOT be included. Remaining params are sorted
    alphabetically by key (UTF-8 byte order) and joined as
    ``key=value`` lines separated by ``\\n``.
    """
    filtered = {k: v for k, v in params.items() if k != "hash"}
    sorted_keys = sorted(filtered.keys(), key=lambda k: k.encode("utf-8"))
    return "\n".join(f"{k}={filtered[k]}" for k in sorted_keys)


def compute_hmac_hash(data_check_string: str, bot_secret: str) -> str:
    """Compute HMAC-SHA256 of the data-check-string using the bot secret."""
    return hmac.new(
        bot_secret.encode("utf-8"),
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_init_data(init_data: str, bot_token: str) -> dict[str, Any]:
    """
    Cryptographically verify Telegram WebApp initData and return the
    parsed payload if valid.

    Args:
        init_data: Raw query string received from the Telegram WebApp client.
        bot_token: Full bot token in the form ``<bot_id>:<bot_secret>``.

    Returns:
        Parsed initData fields (excluding the ``hash``) as a dictionary with
        appropriately typed values.

    Raises:
        TelegramInitDataError: If verification fails for any reason.
    """
    if not bot_token or ":" not in bot_token:
        raise TelegramInitDataError(
            "TELEGRAM_BOT_TOKEN is not configured or has an invalid format"
        )

    # Extract the bot secret (the part after the colon) for HMAC key.
    # The bot token format is: <bot_id>:<bot_secret>
    _bot_id, bot_secret = bot_token.split(":", 1)

    params = parse_init_data(init_data)

    received_hash = params.pop("hash")

    data_check_string = compute_data_check_string(params)
    hmac_hash = compute_hmac_hash(data_check_string, bot_secret)

    if not hmac.compare_digest(hmac_hash, received_hash):
        raise TelegramInitDataError("initData hash verification failed")

    # Optionally validate auth_date freshness to prevent replay attacks.
    # Telegram recommends rejecting auth dates older than a reasonable window.
    _validate_auth_date(params.get("auth_date"))

    return _coerce_types(params)


# Default maximum age for auth_date in seconds (24 hours).
_AUTH_DATE_MAX_AGE_SECONDS = 86400


def _validate_auth_date(auth_date_str: str | None) -> None:
    """
    Validate that the auth_date is not older than the allowed window.

    This mitigates replay attacks where an attacker reuses a previously
    captured valid initData.
    """
    if auth_date_str is None:
        raise TelegramInitDataError("initData missing 'auth_date' field")

    try:
        auth_date = int(auth_date_str)
    except ValueError:
        raise TelegramInitDataError("initData 'auth_date' is not a valid integer")

    import time

    now = int(time.time())
    if now - auth_date > _AUTH_DATE_MAX_AGE_SECONDS:
        raise TelegramInitDataError(
            f"initData 'auth_date' is too old (max {_AUTH_DATE_MAX_AGE_SECONDS}s)"
        )


def _coerce_types(params: dict[str, str]) -> dict[str, Any]:
    """
    Convert raw string values to their appropriate Python types.

    Known Telegram fields and their expected types:
    - id, user, chat, etc. -> int
    - query_id, start_param, etc. -> str (kept as-is)
    """
    result: dict[str, Any] = dict(params)

    # Known integer fields
    int_fields = {"id", "user", "chat", "query_id", "auth_date"}
    for field_name in int_fields:
        if field_name in result and result[field_name] != "":
            try:
                result[field_name] = int(result[field_name])
            except (ValueError, TypeError):
                raise TelegramInitDataError(
                    f"initData field '{field_name}' is not a valid integer"
                )

    return result
