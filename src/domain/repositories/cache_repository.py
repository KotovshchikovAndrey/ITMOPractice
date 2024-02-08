import typing as tp
from abc import abstractmethod
from uuid import UUID

from domain.models.city_point import BaseCityPointsCache, CityPointsCache
from domain.models.user import BaseUserFavoritePointCache, UserFavoritePointCache


class ICacheRepository(tp.Protocol):
    @abstractmethod
    async def get_city_points_cache(
        self, city_pk: UUID
    ) -> tp.Optional[BaseCityPointsCache]: ...

    @abstractmethod
    async def set_city_points_cache(self, city_points: CityPointsCache) -> None: ...

    @abstractmethod
    async def clear_city_points_cache(self) -> None: ...

    @abstractmethod
    async def get_user_favorite_points_cache(
        self, user_pk: UUID
    ) -> tp.Optional[BaseUserFavoritePointCache]: ...

    @abstractmethod
    async def set_user_favorite_points_cache(
        self, user_favorite_points: UserFavoritePointCache
    ) -> None: ...

    @abstractmethod
    async def clear_user_favorite_points_cache(self) -> None: ...
