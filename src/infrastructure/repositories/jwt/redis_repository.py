import typing as tp

import redis.asyncio as aioredis
from kink import inject

from domain.repositories.jwt_repository import IJwtRepository
from infrastructure.database.redis.connection import RedisConnection


@inject(alias=IJwtRepository)
class RedisJwtRepository(IJwtRepository):
    _connection: aioredis.Redis
    _jwt_prefix: str = "jwt"

    def __init__(self, connection: RedisConnection) -> None:
        self._connection = connection.get_connection()

    async def get_jwt_by_hash(self, jwt_hash: str):
        return await self._connection.get(self._get_name_of_jwt(jwt_hash))

    async def set_jwt(self, jwt_hash: str, jwt: str, ttl: int):
        await self._connection.set(
            name=self._get_name_of_jwt(jwt_hash),
            value=jwt,
            ex=ttl,
        )

    async def delete_jwt(self, jwt_hash: str) -> None:
        await self._connection.delete(self._get_name_of_jwt(jwt_hash))

    def _get_name_of_jwt(self, jwt_hash: str) -> str:
        return f"{self._jwt_prefix}:{jwt_hash}"
