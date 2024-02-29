from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from fastapi_users.config.app import app_config

async_engine: AsyncEngine = create_async_engine(
    url=app_config.async_database_url,
    pool_pre_ping=True,
)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=async_engine) as async_session:
        yield async_session
