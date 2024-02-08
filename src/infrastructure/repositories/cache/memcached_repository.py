import json
import typing as tp
from datetime import datetime
from uuid import UUID

import aiomcache
from kink import inject

from domain.models.city_point import BaseCityPointsCache, CityPointsCache
from domain.models.user import BaseUserFavoritePointCache, UserFavoritePointCache
from domain.repositories.cache_repository import ICacheRepository
from infrastructure.config.settings import settings


@inject(alias=ICacheRepository)
class InMemoryCacheRepository(ICacheRepository):
    _connection: aiomcache.Client

    _city_points_prefix: str = "city_points"
    _user_favorite_points_prefix: str = "user_favorite_points"

    def __init__(self) -> None:
        self._connection = aiomcache.Client(
            host=settings.memcached_host,
            port=settings.memcached_port,
        )

    async def get_city_points_cache(self, city_pk: UUID):
        key = f"{self._city_points_prefix}:{city_pk}"
        city_points = await self._connection.get(key=key.encode())
        if city_points is not None:
            data = {
                "city_pk": str(city_pk),
                **json.loads(city_points.decode()),
            }

            return BaseCityPointsCache.model_validate(data)

    async def set_city_points_cache(self, city_points: CityPointsCache):
        key = f"{self._city_points_prefix}:{city_points.city_pk}"
        cached_value = city_points.model_dump_json(include=("points",))
        await self._connection.set(
            key=key.encode(),
            value=cached_value.encode(),
            exptime=city_points.ttl,
        )

    async def clear_city_points_cache(self):
        unixtime = datetime.utcnow().timestamp()
        self._city_points_prefix = f"city_points{unixtime}"
        print("city points cache cleaned up!")

    async def get_user_favorite_points_cache(self, user_pk: UUID):
        key = f"{self._user_favorite_points_prefix}:{user_pk}"
        user_favorite_points = await self._connection.get(key=key.encode())
        if user_favorite_points is not None:
            data = {
                "user_pk": str(user_pk),
                **json.loads(user_favorite_points.decode()),
            }

            return BaseUserFavoritePointCache.model_validate(data)

    async def set_user_favorite_points_cache(
        self, user_favorite_points: UserFavoritePointCache
    ):
        key = f"{self._user_favorite_points_prefix}:{user_favorite_points.user_pk}"
        cached_value = user_favorite_points.model_dump_json(include=("points",))
        await self._connection.set(
            key=key.encode(),
            value=cached_value.encode(),
            exptime=user_favorite_points.ttl,
        )

    async def clear_user_favorite_points_cache(self):
        unixtime = datetime.utcnow().timestamp()
        self._user_favorite_points_prefix = f"user_favorite_points{unixtime}"
        print("favorite points cache cleaned up!")
