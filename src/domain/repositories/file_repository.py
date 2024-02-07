import typing as tp
from io import BytesIO
from abc import abstractmethod


class IFileRepository(tp.Protocol):
    @abstractmethod
    async def save_file(self, file: BytesIO, file_ext: str) -> str:
        """Return file url"""

    @abstractmethod
    async def get_file(self, file_url: str) -> BytesIO: ...
