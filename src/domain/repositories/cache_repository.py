import typing as tp
from abc import abstractmethod
from uuid import UUID

from domain.models.city_point import BaseCityPointsCache, CityPointsCache


class ICacheRepository(tp.Protocol):
    @abstractmethod
    async def get_city_points_cache(self, city_pk: UUID) -> BaseCityPointsCache:
        ...

    @abstractmethod
    async def set_city_points_cache(self, city_points: CityPointsCache) -> None:
        ...
