import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.main import app
from app.db import Base, get_db
# Import functions required for testing
from app.auth.auth import hash_password, verify_password, create_access_token
from app.models import User
import os

os.environ["TESTING"] = "1"
# Use async in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)

# # Async DB override
# async def override_get_db():
#     async with TestingSessionLocal() as session:
#         yield session

# app.dependency_overrides[get_db] = override_get_db
# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def prepare_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest_asyncio.fixture
# async def client():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client

@pytest_asyncio.fixture(scope="function")
async def session():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Provide the session
    async with TestingSessionLocal() as s:
        yield s

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(session: AsyncSession):
    # Override get_db so routes use THIS SAME session
    async def _override_get_db():
        yield session

    app.dependency_overrides[get_db] = _override_get_db

    # Use AsyncClient so we can do async requests
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    # Clean up override
    app.dependency_overrides.clear()