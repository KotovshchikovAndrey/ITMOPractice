import typing as tp
from uuid import UUID
from abc import abstractmethod

from domain.models.city_point import CityPointsCache, BaseCityPointsCache


class ICacheRepository(tp.Protocol):
    @abstractmethod
    async def get_city_points_cache(self, city_pk: UUID) -> BaseCityPointsCache: ...

    @abstractmethod
    async def set_city_points_cache(self, city_points: CityPointsCache) -> None: ...
