import typing as tp
from abc import abstractmethod

from uuid import UUID
from domain.models.city_point import (
    CityInDb,
    PointInDb,
    PointWithTag,
)


class ICityPointRepository(tp.Protocol):
    @abstractmethod
    async def get_cities(self, limit: int, offset: int) -> tp.List[CityInDb]: ...

    @abstractmethod
    async def get_city_by_pk(self, city_pk: UUID) -> tp.Optional[CityInDb]: ...

    @abstractmethod
    async def create_city(self, city: CityInDb) -> UUID: ...

    @abstractmethod
    async def get_city_points_with_tag(
        self, city_pk: UUID
    ) -> tp.List[PointWithTag]: ...

    @abstractmethod
    async def create_point(self, point: PointInDb) -> UUID: ...

    # @abstractmethod
    # async def delete_point(self, point_pk: UUID) -> None: ...

    # @abstractmethod
    # async def get_favorite_points_by_tag(
    #     self, user_pk: UUID, limit: int, offset: int
    # ) -> tp.List[PointInFavorite]: ...

    # @abstractmethod
    # async def create_favorite_point(
    #     self, favorite_point: FavoritePointCreate
    # ) -> None: ...

    # @abstractmethod
    # async def delete_favorite_point(self, user_pk: UUID, point_pk: UUID) -> None: ...

    @abstractmethod
    async def get_all_tag_names(self) -> tp.List[str]: ...

    @abstractmethod
    async def create_tags(self, tags: tp.List[str]) -> None: ...

    @abstractmethod
    async def set_tags_for_point(self, tags: tp.List[str], point_pk: UUID) -> None: ...
