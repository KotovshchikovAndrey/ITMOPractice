import typing as tp
from io import BytesIO
from uuid import UUID

from kink import inject

from domain.exceptions.city_not_found import CityNotFound
from domain.exceptions.coordinates_occupied import CoordinatesOccupied
from domain.exceptions.invalid_tags import InvalidTags
from domain.models.city_point import (
    BasePoint,
    CityCreate,
    CityInDb,
    CityPointsCache,
    PointCreate,
    PointInDb,
    TagPoints,
)
from domain.repositories.cache_repository import ICacheRepository
from domain.repositories.city_point_repository import ICityPointRepository
from domain.services.file_service import FileService


@inject
class CityPointService:
    _repository: ICityPointRepository
    _file_service: FileService
    _cache_storage: ICacheRepository

    def __init__(
        self,
        repository: ICityPointRepository,
        file_service: FileService,
        cache_storage: ICacheRepository,
    ) -> None:
        self._repository = repository
        self._file_service = file_service
        self._cache_storage = cache_storage

    async def get_cities(self, limit: int = 10, offset: int = 0):
        return await self._repository.get_cities(limit, offset)

    async def create_city(
        self,
        city: CityCreate,
        image: tp.Optional[BytesIO] = None,
        image_ext: tp.Optional[str] = None,
    ):
        new_city = CityInDb(**city.model_dump())
        if image is not None:
            image_url = await self._file_service.save_file(image, image_ext)
            new_city.set_image_url(image_url)

        return await self._repository.create_city(new_city)

    async def get_city_points_grouped_by_tag(self, city_pk: UUID):
        cache = await self._cache_storage.get_city_points_cache(city_pk)
        if cache is not None:
            return cache.points

        tag_points: tp.Dict[str, BasePoint] = {}
        city_points = await self._repository.get_city_points_with_tag(city_pk)
        for point in city_points:
            if tag_points.get(point.tag_name) is None:
                tag_points[point.tag_name] = []

            tag_points[point.tag_name].append(BasePoint.model_validate(point))

        grouped_city_points: tp.List[TagPoints] = []
        for tag, points in tag_points.items():
            grouped_city_points.append(TagPoints(tag_name=tag, points=points))

        cache = CityPointsCache(city_pk=city_pk, points=grouped_city_points)
        await self._cache_storage.set_city_points_cache(cache)

        return grouped_city_points

    async def create_point(
        self,
        point: PointCreate,
        image: tp.Optional[BytesIO] = None,
        image_ext: tp.Optional[str] = None,
    ):
        if not await self._is_city_exists(point.city_pk):
            raise CityNotFound()

        if not await self._is_tags_valid(point.tags):
            raise InvalidTags()

        if await self._is_coordinates_occupied(point.coordinates):
            raise CoordinatesOccupied()

        new_point = PointInDb(**point.model_dump(exclude=("tags",)))
        if image is not None:
            image_url = await self._file_service.save_file(image, image_ext)
            new_point.set_image_url(image_url)

        new_point_pk = await self._repository.create_point(new_point)
        await self._repository.set_tags_for_point(point.tags, new_point_pk)

        return new_point_pk

    async def create_tags(self, tags: tp.List[str]):
        exists_tags = await self._repository.get_all_tag_names()
        tags_for_create = set(tags).difference(exists_tags)
        await self._repository.create_tags(tags_for_create)

    async def _is_city_exists(self, city_pk: UUID) -> bool:
        city = await self._repository.get_city_by_pk(city_pk)
        return city is not None

    async def _is_coordinates_occupied(
        self, coordinates: tp.Tuple[float, float]
    ) -> bool:
        point = await self._repository.get_point_by_coordinates(coordinates)
        return point is not None

    async def _is_tags_valid(self, tags: tp.List[str]) -> bool:
        allowed_tags = await self._repository.get_all_tag_names()
        return len(set(tags).difference(allowed_tags)) == 0
