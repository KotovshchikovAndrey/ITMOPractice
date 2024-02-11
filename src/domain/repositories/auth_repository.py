import typing as tp
from abc import abstractmethod
from uuid import UUID


class IAuthRepository(tp.Protocol):
    @abstractmethod
    async def is_user_token_exists(self, user_pk: UUID, token: str) -> bool:
        ...

    @abstractmethod
    async def set_user_token(self, user_pk: UUID, token: str, ttl: int) -> None:
        ...

    @abstractmethod
    async def delete_user_token(self, user_pk: UUID, token: str) -> None:
        ...

    @abstractmethod
    async def delete_expired_user_tokens(self, user_pk: UUID) -> None:
        ...

    @abstractmethod
    async def get_user_login_code(self, user_pk: UUID) -> tp.Optional[str]:
        ...

    @abstractmethod
    async def set_user_login_code(self, user_pk: UUID, code: str, ttl: int) -> None:
        ...

    @abstractmethod
    async def delete_user_login_code(self, user_pk: UUID) -> None:
        ...
