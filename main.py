import uvicorn

from fastapi import FastAPI
from api import all_routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
import services
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from apscheduler.schedulers.asyncio import AsyncIOScheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://bikeland_redis")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # FastAPICache.init(InMemoryBackend())
    """func on start up project"""
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(services.parser_service.check_products_from_1c, 'cron', hour = f"{settings.HOUR}", minute = f"{settings.MINUTE}")
    scheduler.add_job(services.parser_service.auto_delete_product, 'cron', hour=3, minute=0)
    scheduler.start()
    yield





app = FastAPI(title="BIKELAND API", lifespan=lifespan)
add_pagination(app)

app.mount(f"/{settings.media_filename}", StaticFiles(directory=f"{settings.media_filename}"), name=f"{settings.media_filename}")
disable_installed_extensions_check()

for router in all_routers:
    app.include_router(router, prefix=settings.api_v1_prefix)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
