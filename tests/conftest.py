import os
from unittest.mock import AsyncMock
from pathlib import Path


import pytest
import pg8000.native
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from alembic.config import Config
from alembic import command

os.environ.update(
    {
        "APP_CONFIG__DB__URL": "postgresql+asyncpg://webnovel_test:password@localhost:5432/webnovel_test",
    }
)

from core.config import settings

here = Path(__file__).resolve()
alembic_ini = here.parent.parent / "src" / "alembic.ini"


def is_postgres_responsive(
    host: str,
    port: int,
    user: str,
    password: str,
    db: str,
):
    def check():
        try:
            conn = pg8000.connect(
                user=user,
                host=host,
                port=port,
                password=password,
                database=db,
            )
            conn.close()
            return True
        except Exception:
            return False

    return check


@pytest.fixture(scope="session")
async def wait_for_postgres(docker_services):

    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=1.0,
        check=is_postgres_responsive(
            user="webnovel_test",
            host="localhost",
            port=5432,
            password="password",
            db="webnovel_test",
        ),
    )


def run_alembic_migration(
    conn: Connection,
    alembic_ini_path: Path = alembic_ini,
    revision: str = "head",
):
    config = Config(alembic_ini_path)
    command.upgrade(config, revision)


@pytest.fixture(scope="session")
async def test_engine(wait_for_postgres):
    engine = create_async_engine(
        url=str(settings.db.url),
        echo=False,
    )

    async with engine.connect() as conn:
        await conn.run_sync(run_alembic_migration)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def session_maker(test_engine):
    session_maker = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return session_maker


@pytest.fixture()
async def test_session(session_maker):
    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture()
def mock_session():
    return AsyncMock()
