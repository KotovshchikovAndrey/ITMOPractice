import json
import typing as tp
from uuid import UUID

import aiomcache
from kink import inject

from domain.models.city_point import BaseCityPointsCache, CityPointsCache
from domain.repositories.cache_repository import ICacheRepository
from infrastructure.config.settings import settings


@inject(alias=ICacheRepository)
class InMemoryCacheRepository(ICacheRepository):
    _connection: aiomcache.Client

    def __init__(self) -> None:
        self._connection = aiomcache.Client(
            host=settings.memcached_host,
            port=settings.memcached_port,
        )

    async def get_city_points_cache(self, city_pk: UUID) -> BaseCityPointsCache:
        city_points = await self._connection.get(key=str(city_pk).encode())
        if city_points is not None:
            data = {"city_pk": str(city_pk), "points": json.loads(city_points.decode())}
            return BaseCityPointsCache.model_validate(data)

    async def set_city_points_cache(self, city_points: CityPointsCache):
        cached_value = city_points.model_dump(exclude=("city_pk", "ttl"))
        await self._connection.set(
            key=str(city_points.city_pk).encode(),
            value=json.dumps(cached_value["points"]).encode(),
            exptime=city_points.ttl,
        )
