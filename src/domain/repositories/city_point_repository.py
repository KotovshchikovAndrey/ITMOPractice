import typing as tp
from abc import abstractmethod


class ICityPointRepository(tp.Protocol):
    @abstractmethod
    async def test_init(self):
        ...
