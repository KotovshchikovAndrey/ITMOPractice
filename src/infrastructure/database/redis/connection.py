import typing as tp

import redis.asyncio as aioredis

from infrastructure.config.settings import settings
from infrastructure.database.redis.dto import RedisConnectionDTO


class RedisConnection:
    _connection: aioredis.Redis = None
    _connection_config: RedisConnectionDTO

    def __init__(self, connection_config: RedisConnectionDTO) -> None:
        self._connection_config = connection_config

    async def connect(self) -> None:
        if self._connection is not None:
            return

        self._connection = await aioredis.from_url(
            f"redis://{settings.redis_host}:{settings.redis_port}",
            password=settings.redis_password,
            decode_responses=True,
        )

    def get_connection(self) -> aioredis.Redis:
        return self._connection

    async def close(self) -> None:
        await self._connection.close()
