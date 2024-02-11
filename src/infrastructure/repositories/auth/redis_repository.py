import typing as tp
from datetime import datetime
from uuid import UUID

import redis.asyncio as aioredis
from kink import inject

from domain.repositories.auth_repository import IAuthRepository
from infrastructure.database.redis.connection import RedisConnection


@inject(alias=IAuthRepository)
class RedisAuthRepository(IAuthRepository):
    _connection: aioredis.Redis

    _user_tokens_prefix: str = "user_tokens"
    _login_codes_prefix: str = "login_codes"

    def __init__(self, connection: RedisConnection) -> None:
        self._connection = connection.get_connection()

    async def is_user_token_exists(self, user_pk: UUID, token: str):
        score = await self._connection.zscore(
            name=self._get_name_of_user_tokens(user_pk),
            value=token,
        )

        print(score)
        return score is not None

    async def set_user_token(self, user_pk: UUID, token: str, ttl: int):
        score = datetime.utcnow().timestamp() + ttl
        await self._connection.zadd(
            name=self._get_name_of_user_tokens(user_pk),
            mapping={token: score},
        )

    async def delete_user_token(self, user_pk: UUID, token: str):
        await self._connection.zrem(self._get_name_of_user_tokens(user_pk), token)

    async def delete_expired_user_tokens(self, user_pk: UUID):
        await self._connection.zremrangebyscore(
            name=self._get_name_of_user_tokens(user_pk),
            min=0,
            max=datetime.utcnow().timestamp(),
        )

    async def get_user_login_code(self, user_pk: UUID):
        return await self._connection.get(self._get_key_of_user_login_code(user_pk))

    async def set_user_login_code(self, user_pk: UUID, code: int, ttl: int):
        await self._connection.set(
            name=self._get_key_of_user_login_code(user_pk),
            value=code,
            ex=ttl,
        )

    async def delete_user_login_code(self, user_pk: UUID):
        await self._connection.delete(self._get_key_of_user_login_code(user_pk))

    def _get_name_of_user_tokens(self, user_pk: UUID) -> str:
        return f"{self._user_tokens_prefix}:{user_pk}"

    def _get_key_of_user_login_code(self, user_pk: UUID) -> str:
        return f"{self._login_codes_prefix}:{user_pk}"
