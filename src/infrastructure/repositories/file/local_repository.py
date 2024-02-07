import pathlib
import hashlib
from io import BytesIO
from aiofile import async_open
from domain.repositories.file_repository import IFileRepository


class LocalFileRepository(IFileRepository):
    _upload_path = pathlib.Path(".") / "common" / "media"

    async def save_file(self, file: BytesIO, file_ext: str):
        file_hash = hashlib.sha3_256(file.getvalue()).digest().hex()
        filename = f"{file_hash}.{file_ext}"
        file_path = self._upload_path / filename
        if file_path.exists():
            return f"/{filename}"

        async with async_open(file_path, "wb") as afp:
            await afp.write(file.getvalue())

        return f"/{filename}"

    async def get_file(self, file_url: str):
        file_path = self._upload_path / file_url[1:]
        file_buffer = BytesIO()
        async with async_open(file_path, "rb") as afs:
            file_buffer.write(await afs.read())

        return file_buffer
