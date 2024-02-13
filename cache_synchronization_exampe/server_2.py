import asyncio
from contextlib import asynccontextmanager
from pydantic import BaseModel
import uvicorn
from broadcaster import Broadcast
from fastapi import FastAPI
import redis.asyncio as aioredis


redis_cache = aioredis.from_url(
    "redis://127.0.0.1:6579",
    decode_responses=True,
)  # redis-2

broadcast = Broadcast("redis://127.0.0.1:6379")


class CacheEvent(BaseModel):
    event: str
    key: str
    value: str = ""

    class Config:
        from_attributes = True


async def cache_consumer():
    async with broadcast.subscribe(channel="cacheroom") as subscriber:
        async for data in subscriber:
            cache_event = CacheEvent.model_validate_json(data.message)
            match (cache_event.event):
                case "write":
                    await redis_cache.set(name=cache_event.key, value=cache_event.value)
                case "delete":
                    await redis_cache.delete(cache_event.key)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    loop = asyncio.get_running_loop()
    loop.create_task(cache_consumer())
    yield
    await broadcast.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/cache/{key}")
async def get_cache(key: str):
    return await redis_cache.get(key)


@app.post("/cache-event")
async def create_cahce_event(cache_event: CacheEvent):
    await broadcast.publish(
        channel="cacheroom",
        message=cache_event.model_dump_json(),
    )

    return 201


if __name__ == "__main__":
    uvicorn.run(
        "server_2:app",
        host="127.0.0.1",
        port=5002,
        reload=True,
    )
