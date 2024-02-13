import typing as tp
from io import BytesIO
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from kink import di

from domain.models.auth import AuthenticatedUser
from domain.models.city_point import CityCreate, PointCreate, TagsCreate
from domain.services.city_point_service import CityPointService
from infrastructure.api.dto import city_point_requests as requests
from infrastructure.api.dto import city_point_responses as responses
from infrastructure.api.middlewares.authentication import authenticate_current_user

router = APIRouter()


@router.get("/cities", response_model=responses.GetCitiesResponse)
async def get_cities(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    limit: tp.Optional[int] = None,
    offset: tp.Optional[int] = None,
):
    cities = await service.get_cities(limit, offset)
    return {"cities": cities}


@router.get("/cities/{city_pk}", response_model=responses.GetCityPointsResponse)
async def get_city_points(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    current_user: tp.Annotated[AuthenticatedUser, Depends(authenticate_current_user)],
    city_pk: UUID,
):
    city, points = (
        await service.get_city_points_grouped_by_tag_merged_with_favorite_points(
            city_pk=city_pk,
            user_pk=current_user.pk,
        )
    )

    return {"city": city, "points": points}


@router.post(
    "/cities",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.CityCreateResponse,
)
async def create_new_city(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    city: tp.Annotated[CityCreate, Depends(requests.CityCreateRequest.as_form)],
    image: tp.Annotated[tp.Optional[UploadFile], File()] = None,
):
    image_content = image_ext = None
    if image is not None:
        image_content = BytesIO(await image.read())
        image_ext = image.filename.split(".")[-1]

    city_pk = await service.create_city(city, image_content, image_ext)
    return {
        "message": "Город успешно создан!",
        "city_pk": city_pk,
    }


@router.get("/points/{point_pk}", response_model=responses.PointDetailResponse)
async def get_point_detail(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    point_pk: UUID,
):
    point = await service.get_point_detail(point_pk)
    return {"point": point}


@router.post(
    "/points",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.PointCreateResponse,
)
async def create_new_point(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    point: tp.Annotated[PointCreate, Depends(requests.PointCreateRequest.as_form)],
    image: tp.Annotated[tp.Optional[UploadFile], File()] = None,
):
    image_content = image_ext = None
    if image is not None:
        image_content = BytesIO(await image.read())
        image_ext = image.filename.split(".")[-1]

    point_pk = await service.create_point(point, image_content, image_ext)
    return {
        "message": "Городская точка успешно создана!",
        "point_pk": point_pk,
    }


@router.post(
    "/tags",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.SuccessMessageResponse,
)
async def create_tags(
    service: tp.Annotated[CityPointService, Depends(lambda: di[CityPointService])],
    tags: TagsCreate,
):
    await service.create_tags(tags.tags)
    return {"message": "Теги успешно созданы!"}
