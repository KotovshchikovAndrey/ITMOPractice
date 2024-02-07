import typing as tp
from io import BytesIO
import hashlib

from kink import inject
from domain.repositories.file_repository import IFileRepository


@inject
class FileService:
    _repository: IFileRepository

    def __init__(self, repository: IFileRepository) -> None:
        self._repository = repository

    async def save_file(self, file: BytesIO, file_ext: str):
        """Return file url"""

        filename = self._get_filename_from_hash(file, file_ext)
        return await self._repository.save_file(file, filename)

    async def get_file(self, file_url: str):
        return await self._repository.get_file(file_url)

    def _get_filename_from_hash(file: BytesIO, file_ext: str) -> str:
        filehash = hashlib.sha3_256(file.getvalue()).digest().hex()
        return f"{filehash}.{file_ext}"
