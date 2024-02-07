import typing as tp
from uuid import UUID

from fastapi import APIRouter, Depends, status, UploadFile, Form, File
from kink import di

from domain.models.city_point import PointCreate, CityCreate, TagsCreate
from domain.services.city_point_service import CityPointService
from infrastructure.config.settings import settings

router = APIRouter(prefix=f"{settings.api_prefix}")


@router.get("/city")
async def get_cities(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    limit: tp.Optional[int] = None,
    offset: tp.Optional[int] = None,
):
    cities = await service.get_cities(limit, offset)
    return {"cities": cities}


@router.post("/city", status_code=status.HTTP_201_CREATED)
async def create_new_city(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    name: tp.Annotated[str, Form()],
    description: tp.Annotated[tp.Optional[str], Form()] = None,
    image: tp.Annotated[tp.Optional[UploadFile], File()] = None,
):
    image_content = None
    image_ext = None
    if image is not None:
        image_content = image.file
        image_ext = image.filename.split(".")[-1]

    city = CityCreate(name=name, description=description)
    city_pk = await service.create_city(city, image_ext, image_content)
    return {
        "message": "City success created!",
        "city_pk": city_pk,
    }


@router.get("/point")
async def get_grouped_points(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    city_pk: UUID,
):
    points = await service.get_city_points_grouped_by_tag(city_pk)
    return {"points": points}


@router.post("/point", status_code=status.HTTP_201_CREATED)
async def create_new_point(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    point: PointCreate,
):
    point_pk = await service.create_point(point)
    return {
        "message": "Point success created!",
        "point_pk": point_pk,
    }


@router.post("/tag", status_code=status.HTTP_201_CREATED)
async def create_tags(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    tags: TagsCreate,
):
    await service.create_tags(tags.tags)
    return {"message": "Tags success created!"}
