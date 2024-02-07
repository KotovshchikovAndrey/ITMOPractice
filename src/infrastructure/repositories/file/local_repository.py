import pathlib
import hashlib
from io import BytesIO
from aiofile import async_open
from kink import inject
from domain.repositories.file_repository import IFileRepository


@inject(alias=IFileRepository)
class LocalFileRepository(IFileRepository):
    _upload_path = pathlib.Path(".") / "common" / "assets"

    def __init__(self) -> None:
        super().__init__()

    async def save_file(self, file: BytesIO, filename: str):
        file_path = self._upload_path / filename
        if file_path.exists():
            return f"/{filename}"

        async with async_open(file_path.absolute(), "wb") as afp:
            await afp.write(file.getvalue())

        return f"/{filename}"

    async def get_file(self, file_url: str):
        file_path = self._upload_path.joinpath(file_url)
        file_buffer = BytesIO()
        async with async_open(file_path.absolute(), "rb") as afs:
            file_buffer.write(await afs.read())

        return file_buffer
