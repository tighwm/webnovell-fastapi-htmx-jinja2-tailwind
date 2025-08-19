import os
from unittest.mock import AsyncMock
from pathlib import Path

import pytest
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.config import Config
from alembic import command

from tests import database

os.environ.update(
    {
        "APP_CONFIG__DB__URL": "postgresql+asyncpg://webnovel_test:password@localhost:5432/webnovel_test",
    }
)

from core.config import settings

here = Path(__file__).resolve()
alembic_ini = here.parent.parent / "src" / "alembic.ini"


def run_alembic_migration(
    conn: Connection,
    alembic_ini_path: Path = alembic_ini,
    revision: str = "head",
):
    config = Config(alembic_ini_path)
    command.upgrade(config, revision)


@pytest.fixture(scope="session", autouse=True)
async def engine():
    engine = create_async_engine(
        url=str(settings.db.url),
        echo=False,
    )

    async with engine.connect() as conn:
        await conn.run_sync(run_alembic_migration)

    database.async_scoped_session.configure(bind=engine)
    yield
    await engine.dispose()


@pytest.fixture()
async def test_session():
    session = database.async_scoped_session()
    yield session
    await session.rollback()


@pytest.fixture()
def mock_session():
    return AsyncMock()
