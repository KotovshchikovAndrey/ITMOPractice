import typing as tp
from abc import abstractmethod
from io import BytesIO


class IFileRepository(tp.Protocol):
    @abstractmethod
    async def save_file(self, file: BytesIO, filename: str) -> str:
        """Return file url"""

    @abstractmethod
    async def get_file(self, file_url: str) -> BytesIO:
        ...
