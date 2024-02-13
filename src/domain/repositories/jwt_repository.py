import typing as tp
from abc import abstractmethod


class IJwtRepository(tp.Protocol):
    @abstractmethod
    async def get_jwt_by_hash(self, jwt_hash: str) -> tp.Optional[str]: ...

    @abstractmethod
    async def set_jwt(self, jwt_hash: str, jwt: str, ttl: int) -> None: ...

    @abstractmethod
    async def delete_jwt(self, jwt_hash: str) -> None: ...
