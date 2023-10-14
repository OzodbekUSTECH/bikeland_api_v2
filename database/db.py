from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool


engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO, pool_pre_ping=True, poolclass=AsyncAdaptedQueuePool)
session_maker = async_sessionmaker(engine,autoflush=False, autocommit=False, expire_on_commit=False) # 
 

