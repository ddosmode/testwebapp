from uuid import UUID

from app.application.common import UnitOfWork
from app.domain.shared.exceptions import EntityNotFoundError
from app.domain.users.entities import User


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_user(self, user_id: UUID) -> User:
        async with self._uow:
            user = await self._uow.users.get(user_id)
            if user is None:
                raise EntityNotFoundError(f"User {user_id} not found")
            return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        async with self._uow:
            return await self._uow.users.get_by_telegram_id(telegram_id)

    async def create_user(self, user: User) -> None:
        async with self._uow:
            await self._uow.users.add(user)
            await self._uow.commit()

    async def update_user(self, user: User) -> None:
        async with self._uow:
            await self._uow.users.update(user)
            await self._uow.commit()
