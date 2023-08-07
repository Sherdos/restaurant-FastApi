import asyncio
from typing import AsyncGenerator, Generator

import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import AsyncClient
from redis import asyncio as aioredis  # type: ignore
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_HOST,
    REDIS_PORT,
)
from src.database import get_async_session
from src.main import app
from src.menu.models import Base

DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}test'
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator:
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
async def menu_data():
    return {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }


@pytest.fixture
async def submenu_data():
    return {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }


@pytest.fixture
async def dish_data():
    return {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }


@pytest.fixture
async def update_menu_data():
    return {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }


@pytest.fixture
async def update_submenu_data():
    return {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }


@pytest.fixture
async def update_dish_data():
    return {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
        'price': '14.22'
    }
