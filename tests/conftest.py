from dotenv import load_dotenv
load_dotenv()
import sys
import os
import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import text

# Ensure backend is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app.main import app
from app.models.db import get_db

# Use SQLite in-memory DB for async tests
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
AsyncTestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Create builds table for tests
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.execute(text("""
        CREATE TABLE builds (
            github_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TIMESTAMP NOT NULL,
            repo TEXT NOT NULL,
            branch TEXT NOT NULL,
            status TEXT NOT NULL,
            finished_at TIMESTAMP,
            duration_seconds FLOAT
        );
        """))
        await conn.execute(text("""
        CREATE TABLE build_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            github_run_id INTEGER NOT NULL,
            sent_at TIMESTAMP NOT NULL,
            UNIQUE(github_run_id)
        );
        """))
    yield
    # No teardown needed for in-memory DB

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with AsyncTestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    # Override get_db dependency to use test session
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
