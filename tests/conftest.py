
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.db.models.user import User


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/test_coffee"


# Create test database engine
test_engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


# DB dependency for testing
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Override the app's DB dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db() -> AsyncGenerator[None, None]:
    # Create the test database and tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop the test database after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
def client(test_db) -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    # Create a test user
    hashed_password = get_password_hash("password123")
    user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone="1234567890",
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True,
        role="user"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_admin(db_session: AsyncSession) -> User:
    # Create a test admin user
    hashed_password = get_password_hash("admin123")
    admin = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        hashed_password=hashed_password,
        is_active=True,
        is_verified=True,
        role="admin"
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
def user_token(test_user: User) -> str:
    # Create a token for the test user
    access_token = create_access_token({"sub": str(test_user.id)})
    return access_token


@pytest.fixture
def admin_token(test_admin: User) -> str:
    # Create a token for the test admin
    access_token = create_access_token({"sub": str(test_admin.id)})
    return access_token
