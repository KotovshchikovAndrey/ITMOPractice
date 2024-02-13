import typing as tp
from abc import abstractmethod
from uuid import UUID

from domain.models.city_point import (
    BasePoint,
    CityInDb,
    PointDetail,
    PointInDb,
    PointWithTag,
    Tag,
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
    async def get_point_by_pk(self, point_pk: UUID) -> tp.Optional[PointDetail]: ...

    @abstractmethod
    async def get_point_by_coordinates(
        self, coordinates: tp.Tuple[float, float]
    ) -> tp.Optional[BasePoint]: ...

    @abstractmethod
    async def create_point(self, point: PointInDb) -> UUID: ...

    @abstractmethod
    async def favorite_point_exists(self, user_pk: UUID, point_pk: UUID) -> bool: ...

    @abstractmethod
    async def get_favorite_points_by_city(
        self, user_pk: UUID, city_pk: UUID
    ) -> tp.List[BasePoint]: ...

    @abstractmethod
    async def get_favorite_points_with_tag(
        self, user_pk: UUID
    ) -> tp.List[PointWithTag]: ...

    @abstractmethod
    async def set_favorite_point(self, user_pk: UUID, point_pk: UUID) -> None: ...

    @abstractmethod
    async def delete_favorite_point(self, user_pk: UUID, point_pk: UUID) -> None: ...

    @abstractmethod
    async def get_all_tag_names(self) -> tp.List[str]: ...

    @abstractmethod
    async def get_tags_by_names(self, tag_names: tp.Set[str]) -> tp.List[Tag]: ...

    @abstractmethod
    async def create_tags(self, tags: tp.Iterable[Tag]) -> None: ...

    @abstractmethod
    async def set_tags_for_point(
        self, tags: tp.Iterable[Tag], point_pk: UUID
    ) -> None: ...
