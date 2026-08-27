import pytest_asyncio

from app.infrastructure.database.session import SessionFactory


@pytest_asyncio.fixture
async def session():
    async with SessionFactory() as session:
        yield session
