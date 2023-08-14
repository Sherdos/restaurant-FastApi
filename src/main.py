from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis  # type: ignore

from src.config import REDIS_HOST, REDIS_PORT
from src.menu.router import router_dish, router_menu, router_submenu

app = FastAPI(
    title='Menu API'
)


app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)


@app.on_event('startup')
async def startup_event() -> None:
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
