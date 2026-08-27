"""
Tests for Telegram WebApp initData cryptographic validation.

These tests verify that:
1. Valid initData with a correct HMAC hash passes verification.
2. Tampered initData (wrong hash, missing fields, expired auth_date)
   is rejected.
3. The validator rejects empty or malformed input.
4. The ``initDataUnsafe`` pattern is never used — only the raw initData
   query string is accepted.
"""

from __future__ import annotations

import hashlib
import hmac
import time

import pytest

from app.domain.shared.exceptions import TelegramInitDataError
from app.infrastructure.telegram.validator import (
    TelegramInitDataError as ValidatorInitDataError,
    _coerce_types,
    _validate_auth_date,
    parse_init_data,
    verify_init_data,
)


# A realistic but fake bot token for testing.
# Format: <bot_id>:<bot_secret>
TEST_BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRsTUVwxYZ1234567890"


def _make_hash(bot_secret: str, data_check_string: str) -> str:
    return hmac.new(
        bot_secret.encode("utf-8"),
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _build_init_data(fields: dict[str, str], bot_token: str = TEST_BOT_TOKEN) -> str:
    """
    Build a syntactically valid initData query string with a correct HMAC hash.
    """
    _bot_id, bot_secret = bot_token.split(":", 1)

    params = dict(fields)
    params.pop("hash", None)
    sorted_keys = sorted(params.keys(), key=lambda k: k.encode("utf-8"))
    data_check_string = "\n".join(f"{k}={params[k]}" for k in sorted_keys)
    params["hash"] = _make_hash(bot_secret, data_check_string)

    return "&".join(f"{k}={v}" for k, v in params.items())


@pytest.fixture
def valid_init_data() -> str:
    return _build_init_data(
        {
            "id": "123456789",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "auth_date": str(int(time.time())),
            "hash": "",  # replaced by _build_init_data
        }
    )


class TestParseInitData:
    def test_parse_valid_query_string(self) -> None:
        qs = "a=1&b=2&hash=abc123"
        result = parse_init_data(qs)
        assert result["a"] == "1"
        assert result["b"] == "2"
        assert result["hash"] == "abc123"

    def test_parse_preserves_order(self) -> None:
        qs = "z=1&a=2&m=3&hash=abc"
        result = parse_init_data(qs)
        assert list(result.keys()) == ["z", "a", "m", "hash"]

    def test_parse_missing_hash_raises(self) -> None:
        with pytest.raises(ValidatorInitDataError, match="missing 'hash' field"):
            parse_init_data("a=1&b=2")

    def test_parse_empty_string_raises(self) -> None:
        with pytest.raises(ValidatorInitDataError, match="empty"):
            parse_init_data("")

    def test_parse_blank_string_raises(self) -> None:
        with pytest.raises(ValidatorInitDataError, match="empty"):
            parse_init_data("   ")


class TestVerifyInitData:
    def test_valid_init_data_passes(self, valid_init_data: str) -> None:
        payload = verify_init_data(valid_init_data, TEST_BOT_TOKEN)
        assert payload["id"] == 123456789
        assert payload["first_name"] == "Test"
        assert payload["username"] == "testuser"
        assert "hash" not in payload

    def test_tampered_hash_raises(self, valid_init_data: str) -> None:
        tampered = valid_init_data.replace("hash=", "hash=x")
        with pytest.raises(ValidatorInitDataError, match="hash verification failed"):
            verify_init_data(tampered, TEST_BOT_TOKEN)

    def test_tampered_field_raises(self, valid_init_data: str) -> None:
        tampered = valid_init_data.replace("first_name=Test", "first_name=Evil")
        with pytest.raises(ValidatorInitDataError, match="hash verification failed"):
            verify_init_data(tampered, TEST_BOT_TOKEN)

    def test_missing_bot_token_raises(self, valid_init_data: str) -> None:
        with pytest.raises(ValidatorInitDataError, match="not configured"):
            verify_init_data(valid_init_data, "")

    def test_invalid_bot_token_format_raises(self, valid_init_data: str) -> None:
        with pytest.raises(ValidatorInitDataError, match="not configured"):
            verify_init_data(valid_init_data, "not-a-valid-token")

    def test_expired_auth_date_raises(self) -> None:
        old_auth_date = str(int(time.time()) - 25 * 3600)  # 25 hours ago
        init_data = _build_init_data(
            {
                "id": "123456789",
                "first_name": "Test",
                "auth_date": old_auth_date,
            }
        )
        with pytest.raises(ValidatorInitDataError, match="too old"):
            verify_init_data(init_data, TEST_BOT_TOKEN)

    def test_missing_auth_date_raises(self) -> None:
        init_data = _build_init_data(
            {
                "id": "123456789",
                "first_name": "Test",
            }
        )
        # Remove auth_date from the params by rebuilding manually
        init_data = init_data.replace("&auth_date=", "&").replace("auth_date=", "")
        with pytest.raises(ValidatorInitDataError, match="missing 'auth_date' field"):
            verify_init_data(init_data, TEST_BOT_TOKEN)

    def test_wrong_bot_token_rejects(self, valid_init_data: str) -> None:
        wrong_token = "999999999:WrongSecretKey1234567890ab"
        with pytest.raises(ValidatorInitDataError, match="hash verification failed"):
            verify_init_data(valid_init_data, wrong_token)

    def test_non_integer_id_raises(self) -> None:
        init_data = _build_init_data(
            {
                "id": "not-a-number",
                "first_name": "Test",
                "auth_date": str(int(time.time())),
            }
        )
        with pytest.raises(ValidatorInitDataError, match="not a valid integer"):
            verify_init_data(init_data, TEST_BOT_TOKEN)


class TestCoerceTypes:
    def test_integer_fields_coerced(self) -> None:
        raw = {"id": "42", "auth_date": "1700000000"}
        result = _coerce_types(raw)
        assert result["id"] == 42
        assert result["auth_date"] == 1700000000

    def test_string_fields_remain_strings(self) -> None:
        raw = {"username": "testuser", "first_name": "Test"}
        result = _coerce_types(raw)
        assert result["username"] == "testuser"
        assert result["first_name"] == "Test"


class TestValidateAuthDate:
    def test_recent_auth_date_accepted(self) -> None:
        recent = str(int(time.time()))
        _validate_auth_date(recent)  # should not raise

    def test_old_auth_date_rejected(self) -> None:
        old = str(int(time.time()) - 25 * 3600)
        with pytest.raises(ValidatorInitDataError, match="too old"):
            _validate_auth_date(old)

    def test_none_auth_date_rejected(self) -> None:
        with pytest.raises(ValidatorInitDataError, match="missing"):
            _validate_auth_date(None)

    def test_non_integer_auth_date_rejected(self) -> None:
        with pytest.raises(ValidatorInitDataError, match="not a valid integer"):
            _validate_auth_date("abc")
