import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest_asyncio

from app.infrastructure.database import Base
from app.infrastructure.database.session import SessionFactory, engine


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
