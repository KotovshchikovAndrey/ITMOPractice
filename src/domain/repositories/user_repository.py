import typing as tp
from abc import abstractmethod
from uuid import UUID

from domain.models.user import UserInDb


class IUserRepository(tp.Protocol):
    @abstractmethod
    async def get_user_by_pk(self, user_pk: UUID) -> tp.Optional[UserInDb]:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> tp.Optional[UserInDb]:
        ...

    @abstractmethod
    async def create_user(self, user: UserInDb) -> UUID:
        ...
