import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import engine, Base
import asyncio

@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(monkeypatch):
    async def fake_fetch(name: str):
        return {
            "name": name,
            "intelligence": 50,
            "strength": 60,
            "speed": 70,
            "power": 80,
        }
    monkeypatch.setattr("app.routers.hero.fetch_hero_stats", fake_fetch)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c
