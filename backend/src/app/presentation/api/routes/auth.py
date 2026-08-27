from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.application.telegram.services import TelegramAuthService
from app.application.users.services import UserService
from app.config.settings import settings
from app.domain.users.entities import User
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.database.uow import SqlAlchemyUnitOfWork

router = APIRouter(prefix="/auth", tags=["auth"])


class TelegramAuthRequest(BaseModel):
    init_data: str = Field(
        ...,
        description=(
            "Raw Telegram WebApp initData query string. "
            "Obtain from window.Telegram.WebApp.initData in the frontend."
        ),
    )


class TelegramUserResponse(BaseModel):
    id: str
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo_url: str | None = None
    is_admin: bool = False
    is_active: bool = True


class TelegramAuthResponse(BaseModel):
    user: TelegramUserResponse


@router.get("/me")
async def get_me(user_id: UUID) -> dict[str, object]:
    service = UserService(SqlAlchemyUnitOfWork(SessionFactory))

    try:
        user = await service.get_user(user_id)
    except Exception as exc:
        if exc.__class__.__name__ == "EntityNotFoundError":
            raise HTTPException(status_code=404, detail="User not found") from exc
        raise

    return {
        "id": str(user.id),
        "telegram_id": user.telegram_id,
        "username": user.username,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
    }


@router.post("/register")
async def register(telegram_id: int, username: str | None = None) -> dict[str, object]:
    service = UserService(SqlAlchemyUnitOfWork(SessionFactory))
    existing = await service.get_by_telegram_id(telegram_id)
    if existing is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        id=UUID("00000000-0000-0000-0000-000000000000"),
        telegram_id=telegram_id,
        username=username,
    )
    await service.create_user(user)

    return {
        "id": str(user.id),
        "telegram_id": user.telegram_id,
        "username": user.username,
    }


@router.post("/telegram", response_model=TelegramAuthResponse)
async def telegram_auth(request: TelegramAuthRequest) -> TelegramAuthResponse:
    """
    Authenticate a user via Telegram WebApp initData.

    The initData string is cryptographically verified using the bot token
    configured in ``TELEGRAM_BOT_TOKEN``. On success, the user is created
    (if new) or updated (if returning), and their profile is returned.

    **Security**: Never trust ``initDataUnsafe`` on the backend. Only the
    raw ``initData`` query string is accepted and verified.
    """
    if not settings.telegram_bot_token:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: TELEGRAM_BOT_TOKEN is not set",
        )

    async with SqlAlchemyUnitOfWork(SessionFactory) as uow:
        service = TelegramAuthService(uow.users)
        try:
            user = await service.authenticate(request.init_data)
        except Exception as exc:
            if exc.__class__.__name__ in ("TelegramInitDataError", "TelegramAuthError"):
                raise HTTPException(
                    status_code=401,
                    detail=str(exc),
                ) from exc
            raise

        await uow.commit()

    return TelegramAuthResponse(
        user=TelegramUserResponse(
            id=str(user.id),
            telegram_id=user.telegram_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            is_admin=user.is_admin,
            is_active=user.is_active,
        )
    )
