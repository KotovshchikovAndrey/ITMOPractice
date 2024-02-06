import typing as tp
from uuid import UUID

from fastapi import APIRouter, Depends, status
from kink import di

from domain.models.city_point import PointCreate, CityCreate, TagsCreate
from domain.services.city_point_service import CityPointService
from infrastructure.config.settings import settings

router = APIRouter(prefix=f"{settings.api_prefix}")


@router.post("/city", status_code=status.HTTP_201_CREATED)
async def create_new_city(
    city: CityCreate,
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
):
    city_pk = await service.create_city(city)
    return {
        "message": "City success created!",
        "city_pk": city_pk,
    }


@router.get("/point")
async def get_grouped_points(
    city_pk: UUID,
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
):
    points = await service.get_city_points_grouped_by_tag(city_pk)
    return {"points": points}


@router.post("/point", status_code=status.HTTP_201_CREATED)
async def create_new_point(
    point: PointCreate,
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
):
    point_pk = await service.create_point(point)
    return {
        "message": "Point success created!",
        "point_pk": point_pk,
    }


@router.post("/tag", status_code=status.HTTP_201_CREATED)
async def create_tags(
    tags: TagsCreate,
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
):
    await service.create_tags(tags.tags)
    return {"message": "Tags success created!"}
