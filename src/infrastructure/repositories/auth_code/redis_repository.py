import typing as tp
from uuid import UUID

import redis.asyncio as aioredis
from kink import inject

from domain.repositories.auth_code_repository import IAuthCodeRepository
from infrastructure.database.redis.connection import RedisConnection


@inject(alias=IAuthCodeRepository)
class RedisAuthCodeRepository(IAuthCodeRepository):
    _connection: aioredis.Redis
    _login_codes_prefix: str = "login_codes"

    def __init__(self, connection: RedisConnection) -> None:
        self._connection = connection.get_connection()

    async def get_user_login_code(self, user_pk: UUID):
        return await self._connection.get(self._get_name_of_user_login_code(user_pk))

    async def set_user_login_code(self, user_pk: UUID, code: int, ttl: int):
        await self._connection.set(
            name=self._get_name_of_user_login_code(user_pk),
            value=code,
            ex=ttl,
        )

    async def delete_user_login_code(self, user_pk: UUID):
        await self._connection.delete(self._get_name_of_user_login_code(user_pk))

    def _get_name_of_user_login_code(self, user_pk: UUID) -> str:
        return f"{self._login_codes_prefix}:{user_pk}"
