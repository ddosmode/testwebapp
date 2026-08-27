from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.entities import User
from app.infrastructure.database.models.users import UserModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserModel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def add(self, user: User) -> UserModel:  # type: ignore[override]
        user_model = UserModel(
            id=user.id,
            telegram_id=user.telegram_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo_url=user.photo_url,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at if isinstance(user.created_at, datetime) else datetime.utcnow(),
            updated_at=user.updated_at if isinstance(user.updated_at, datetime) else datetime.utcnow(),
        )
        self.session.add(user_model)
        await self.session.flush()
        return user_model

    async def update(self, user: User) -> UserModel:
        existing = await self.get(user.id)
        if existing is None:
            raise ValueError(f"User {user.id} not found")

        existing.username = user.username
        existing.first_name = user.first_name
        existing.last_name = user.last_name
        existing.photo_url = user.photo_url
        existing.is_admin = user.is_admin
        existing.is_active = user.is_active
        existing.updated_at = datetime.utcnow()

        await self.session.flush()
        return existing
