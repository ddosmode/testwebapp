from datetime import datetime

from sqlalchemy import select, update

from app.domain.users.entities import User
from app.infrastructure.database.models.users import UserModel
from app.infrastructure.database.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserModel]):
    def __init__(self, session):
        super().__init__(session, UserModel)

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def add(self, user: User) -> UserModel:
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

    async def update(self, user: UserModel) -> UserModel:
        await self.session.merge(user)
        await self.session.flush()
        return user
