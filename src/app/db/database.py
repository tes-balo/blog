# database.py
from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from app.core.config import settings

# db.py

DATABASE_URL = settings.database_url
# DATABASE_URL = "postgresql+asyncpg://postgres:5248@localhost:5432/blogs"

# Create async engine
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # shows SQL queries in logs (optional)
)


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as conn:
        yield conn


metadata = MetaData()
