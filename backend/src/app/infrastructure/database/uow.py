from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import SessionFactory


class SqlAlchemyUnitOfWork:
    def __init__(self) -> None:
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = SessionFactory()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session is None:
            return

        if exc_type is not None:
            await self.session.rollback()

        await self.session.close()
        self.session = None

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork is not active")

        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork is not active")

        await self.session.rollback()
