import typing as tp
from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from kink import di

from domain.models.city_point import CityCreate, PointCreate, TagsCreate
from domain.services.city_point_service import CityPointService
from infrastructure.api.dto import city_point_responses as responses

router = APIRouter(prefix="/city-point")


@router.get("/city", response_model=responses.GetCitiesResponse)
async def get_cities(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    limit: tp.Optional[int] = None,
    offset: tp.Optional[int] = None,
):
    cities = await service.get_cities(limit, offset)
    return {"cities": cities}


@router.get("/city/{city_pk}", response_model=responses.GetCityPointsResponse)
async def get_city_points(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    city_pk: UUID,
):
    city, points = await service.get_city_points_grouped_by_tag(city_pk)
    return {"city": city, "points": points}


@router.post(
    "/city",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.CityCreateResponse,
)
async def create_new_city(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    name: tp.Annotated[str, Form()],
    description: tp.Annotated[tp.Optional[str], Form()] = None,
    image: tp.Annotated[tp.Optional[UploadFile], File()] = None,
):
    image_content = image_ext = None
    if image is not None:
        image_content = BytesIO(await image.read())
        image_ext = image.filename.split(".")[-1]

    city = CityCreate(name=name, description=description)
    city_pk = await service.create_city(city, image_content, image_ext)
    return {
        "message": "Город успешно создан!",
        "city_pk": city_pk,
    }


@router.get("/point/{point_pk}", response_model=responses.PointDetailResponse)
async def get_point_detail(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    point_pk: UUID,
):
    point = await service.get_point_detail(point_pk)
    return {"point": point}


@router.post(
    "/point",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.PointCreateResponse,
)
async def create_new_point(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    point: PointCreate,
):
    point_pk = await service.create_point(point)
    return {
        "message": "Городская точка успешно создана!",
        "point_pk": point_pk,
    }


@router.post(
    "/tag",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.SuccessMessageResponse,
)
async def create_tags(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    tags: TagsCreate,
):
    await service.create_tags(tags.tags)
    return {"message": "Теги успешно созданы!"}
