import os

import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from app.config import Settings, get_settings
from app.db import get_db_session
from app.main import app, create_application
from app.models.sqlalchemy import Base
from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

settings = get_settings()

DATABASE_TEST_URL = os.environ.get("DATABASE_TEST_URL")


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def test_app_with_db():
    # Create a new session manager for the test DB
    test_sessionmanager = DatabaseSessionManager(DATABASE_TEST_URL, {"echo": False})

    # Dependency override
    async def override_get_db_session():
        async with test_sessionmanager.session() as session:
            yield session

    app = create_application()
    app.dependency_overrides[get_db_session] = override_get_db_session

    # Create tables
    async with test_sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Use httpx.AsyncClient with ASGITransport
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Drop the tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


def run_migrations(connection: Connection):
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic")
    config.set_main_option("sqlalchemy.url", settings.database_url)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": Base.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


# new
@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()  # new
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:  # updated
        # testing
        yield test_client
    # tear down
