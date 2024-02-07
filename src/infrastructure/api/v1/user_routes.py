import typing as tp
from uuid import UUID

from fastapi import APIRouter, Depends
from kink import di

from domain.services.user_service import UserService
from infrastructure.api.dto import user_responses as responses

# Заглушка
USER_PK = "595bf728-7d00-4d17-af56-78c9c5d885ea"

router = APIRouter(prefix="/user")


@router.get("/me/favorite", response_model=responses.MyFavoritePointsResponse)
async def get_my_favorite_points(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])]
):
    favorite_points = await service.get_user_favorite_points(USER_PK)
    return {"favorite_points": favorite_points}


@router.patch(
    "/me/favorite/{point_pk}",
    response_model=responses.SuccessMessageResponse,
)
async def add_point_to_favorite(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    point_pk: UUID,
):
    await service.add_point_to_favorite(USER_PK, point_pk)
    return {"message": "Городская точка добавлена в избранное!"}


@router.delete(
    "/me/favorite/{point_pk}",
    response_model=responses.SuccessMessageResponse,
)
async def delete_point_from_favorite(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    point_pk: UUID,
):
    await service.delete_point_from_favorite(USER_PK, point_pk)
    return {"message": "Городская точка удалена из избранного!"}
