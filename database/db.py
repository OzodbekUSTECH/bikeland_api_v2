from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO, pool_size=10, max_overflow=20)
session_maker = async_sessionmaker(engine,autoflush=False, autocommit=False, expire_on_commit=False) # 
 

