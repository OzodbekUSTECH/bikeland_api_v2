import uvicorn

from fastapi import FastAPI
from api import all_routers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

app = FastAPI(title="Market place by Minzifa Travel")
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


# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(
#         f"{settings.REDIS_URL}",
#         encoding="utf8",
#         decode_responses=True,
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
