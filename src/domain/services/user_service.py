import typing as tp
from uuid import UUID

from kink import inject

from domain.exceptions.email_occupied import EmailOccupied
from domain.exceptions.point_already_in_favorite import PointAlreadyInFavorite
from domain.models.user import UserCreate, UserInDb
from domain.repositories.user_repository import IUserRepository
from domain.services.city_point_service import CityPointService


@inject
class UserService:
    _repository: IUserRepository
    _city_point_service: CityPointService

    def __init__(
        self, repository: IUserRepository, city_point_service: CityPointService
    ) -> None:
        self._repository = repository
        self._city_point_service = city_point_service

    async def get_user_by_pk(self, user_pk: UUID):
        return await self._repository.get_user_by_pk(user_pk)

    async def create_user(self, user: UserCreate):
        if await self._is_email_occupied(user.email):
            raise EmailOccupied()

        new_user = UserInDb(**user.model_dump())
        new_user_pk = await self._repository.create_user(new_user)
        return new_user_pk

    async def get_user_favorite_points(self, user_pk: UUID):
        return await self._city_point_service.get_favorite_points_grouped_by_tag(
            user_pk=user_pk
        )

    async def add_point_to_favorite(self, user_pk: UUID, point_pk: UUID):
        is_favorite_point_exists = (
            await self._city_point_service.is_favorite_point_exists(user_pk, point_pk)
        )

        if is_favorite_point_exists:
            raise PointAlreadyInFavorite()

        await self._city_point_service.set_favorite_point(user_pk, point_pk)

    async def delete_point_from_favorite(self, user_pk: UUID, point_pk: UUID):
        await self._city_point_service.delete_favorite_point(user_pk, point_pk)

    async def _is_email_occupied(self, email: str) -> bool:
        user = await self._repository.get_user_by_email(email)
        return user is not None
