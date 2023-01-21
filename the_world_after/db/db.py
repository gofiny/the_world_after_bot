import contextlib
import logging
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from the_world_after.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()
engine = create_async_engine(
    settings.DB_DSN,
    pool_pre_ping=True,
)
session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@contextlib.asynccontextmanager
async def get_session() -> AsyncSession:
    session: AsyncSession = session_factory()
    try:
        yield session
    finally:
        await session.close()


async def check_session():
    try:
        async with get_session() as session:
            await session.execute(text("SELECT 1"))
    except Exception:
        logger.exception("Unable connect to the database")
        sys.exit(1)
