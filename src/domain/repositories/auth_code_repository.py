import typing as tp
from abc import abstractmethod
from uuid import UUID


class IAuthCodeRepository(tp.Protocol):
    @abstractmethod
    async def get_user_login_code(self, user_pk: UUID) -> tp.Optional[str]: ...

    @abstractmethod
    async def set_user_login_code(self, user_pk: UUID, code: str, ttl: int) -> None: ...

    @abstractmethod
    async def delete_user_login_code(self, user_pk: UUID) -> None: ...
