import typing as tp
from uuid import UUID
from io import BytesIO
from kink import inject

from domain.exceptions.city_not_found import CityNotFound
from domain.exceptions.invalid_tags import InvalidTags

from domain.repositories.city_point_repository import ICityPointRepository
from domain.services.file_service import FileService
from domain.models.city_point import (
    TagPoints,
    CityCreate,
    CityInDb,
    PointInDb,
    PointCreate,
    BasePoint,
)


@inject
class CityPointService:
    _repository: ICityPointRepository
    _file_service: FileService

    def __init__(
        self, repository: ICityPointRepository, file_service: FileService
    ) -> None:
        self._repository = repository
        self._file_service = file_service

    async def get_cities(self, limit: int = 10, offset: int = 0):
        return await self._repository.get_cities(limit, offset)

    async def create_city(
        self,
        city: CityCreate,
        image_ext: tp.Optional[str] = None,
        image: tp.Optional[BytesIO] = None,
    ):
        image_url = None
        if image is not None:
            image_url = await self._file_service.save_file(image, image_ext)

        new_city = CityInDb(**city.model_dump(), image_url=image_url)
        return await self._repository.create_city(new_city)

    async def get_city_points_grouped_by_tag(self, city_pk: UUID):
        tag_points: tp.Dict[str, BasePoint] = {}
        city_points = await self._repository.get_city_points_with_tag(city_pk)
        for point in city_points:
            if tag_points.get(point.tag_name) is None:
                tag_points[point.tag_name] = []

            tag_points[point.tag_name].append(BasePoint.model_validate(point))

        grouped_city_points = []
        for tag, points in tag_points.items():
            grouped_city_points.append(TagPoints(tag_name=tag, points=points))

        return grouped_city_points

    async def create_point(
        self, point: PointCreate, image: tp.Optional[BytesIO] = None
    ):
        if image is not None:
            ...

        city = await self._repository.get_city_by_pk(city_pk=point.city_pk)
        if city is None:
            raise CityNotFound()

        allowed_tags = await self._repository.get_all_tag_names()
        if len(set(point.tags).difference(allowed_tags)) != 0:
            raise InvalidTags()

        new_point = PointInDb(**point.model_dump(exclude=("tags",)))
        new_point_pk = await self._repository.create_point(new_point)
        await self._repository.set_tags_for_point(point.tags, new_point_pk)

        return new_point_pk

    async def create_tags(self, tags: tp.List[str]):
        exists_tags = await self._repository.get_all_tag_names()
        tags_for_create = set(tags).difference(exists_tags)
        await self._repository.create_tags(tags_for_create)
