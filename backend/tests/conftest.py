import pytest_asyncio

from app.infrastructure.database import Base
from app.infrastructure.database.session import engine, SessionFactory


@pytest_asyncio.fixture(autouse=True)
async def _setup_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session():
    async with SessionFactory() as session:
        yield session
