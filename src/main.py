from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis  # type: ignore
from celery.result import AsyncResult
from src.tasks import celery, update_admin_xlsx

from src.config import REDIS_HOST, REDIS_PORT
from src.menu.router import router_menu, router_submenu, router_dish

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



@app.post("/start_task")
async def start_task():
    task_result = update_admin_xlsx.apply_async(countdown=15)
    return {"task_id": task_result.id}

@app.get("/task_status/{task_id}")
async def task_status(task_id: str):
    task = AsyncResult(task_id, app=app)
    return {"status": task.state}