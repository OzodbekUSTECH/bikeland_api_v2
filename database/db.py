from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO, future=True, poolclass=NullPool)
session_maker = async_sessionmaker(engine, autoflush=False, autocommit=False, expire_on_commit=False)


