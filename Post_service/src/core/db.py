from _collections_abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.core.confog import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True,pool_size = 10, max_overflow = 0)

async_session_factory = async_sessionmaker(engine, expire_on_commit = False, class_ = AsyncSession)

class Base(DeclarativeBase):
    pass