import typing as tp
from uuid import UUID

from fastapi import APIRouter, Depends
from kink import di

from domain.models.auth import AuthenticatedUser
from domain.models.user import UserCreate
from domain.services.user_service import UserService
from infrastructure.api.dto import user_responses as responses
from infrastructure.api.middlewares.authentication import authenticate_current_user

router = APIRouter(prefix="/user")


@router.post("/")
async def create_new_user(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    user: UserCreate,
):
    user_pk = await service.create_user(user)
    return {
        "user_pk": user_pk,
        "message": "user success created!",
    }


@router.get("/{user_pk}/favorite", response_model=responses.MyFavoritePointsResponse)
async def get_my_favorite_points(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    current_user: tp.Annotated[AuthenticatedUser, Depends(authenticate_current_user)],
):
    favorite_points = await service.get_user_favorite_points(current_user.pk)
    return {"favorite_points": favorite_points}


@router.patch(
    "/{user_pk}/favorite/{point_pk}",
    response_model=responses.SuccessMessageResponse,
)
async def add_point_to_favorite(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    current_user: tp.Annotated[AuthenticatedUser, Depends(authenticate_current_user)],
    point_pk: UUID,
):
    await service.add_point_to_favorite(current_user.pk, point_pk)
    return {"message": "Городская точка добавлена в избранное!"}


@router.delete(
    "/{user_pk}/favorite/{point_pk}",
    response_model=responses.SuccessMessageResponse,
)
async def delete_point_from_favorite(
    service: tp.Annotated[UserService, Depends(lambda: di[UserService])],
    current_user: tp.Annotated[AuthenticatedUser, Depends(authenticate_current_user)],
    point_pk: UUID,
):
    await service.delete_point_from_favorite(current_user.pk, point_pk)
    return {"message": "Городская точка удалена из избранного!"}
