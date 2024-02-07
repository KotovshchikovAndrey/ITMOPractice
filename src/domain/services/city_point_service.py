import typing as tp
from uuid import UUID
import asyncio
from io import BytesIO
from kink import inject

from domain.exceptions.city_not_found import CityNotFound
from domain.exceptions.invalid_tags import InvalidTags

from domain.repositories.city_point_repository import ICityPointRepository
from domain.models.city_point import (
    TagPoints,
    CityCreate,
    CityInDb,
    PointInDb,
    PointCreate,
)


@inject
class CityPointService:
    _repository: ICityPointRepository

    def __init__(self, repository: ICityPointRepository) -> None:
        self._repository = repository

    async def get_cities(self, limit: int = 10, offset: int = 0):
        return await self._repository.get_cities(limit, offset)

    async def create_city(self, city: CityCreate, image: tp.Optional[BytesIO] = None):
        if image is not None:
            ...

        new_city = CityInDb(**city.model_dump())
        return await self._repository.create_city(new_city)

    async def get_city_points_grouped_by_tag(self, city_pk: UUID):
        tag_names = await self._repository.get_all_tag_names()

        coroutines: tp.List[asyncio.Task[TagPoints]] = []
        async with asyncio.TaskGroup() as tg:
            for tag_name in tag_names:
                coroutine = tg.create_task(
                    self.get_points_by_city_and_tag(city_pk, tag_name)
                )

                coroutines.append(coroutine)

        return [coroutine.result() for coroutine in coroutines]

    async def get_points_by_city_and_tag(self, city_pk: UUID, tag_name: str):
        points = await self._repository.get_points_by_city_and_tag(
            city_pk=city_pk,
            tag_name=tag_name,
        )

        return TagPoints(tag_name=tag_name, points=points)

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
