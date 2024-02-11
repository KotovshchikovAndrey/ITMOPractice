import typing as tp
from contextlib import asynccontextmanager

import asyncpg

from infrastructure.database.postgres.dto import PostgresConnectionDTO


class PostgresMasterConnection:
    _pool_min_size: int = 1
    _pool_max_size: int = 3
    _timeout: int = 30

    _connection_pool: asyncpg.Pool = None

    def __init__(self, connection: PostgresConnectionDTO) -> None:
        self.connection = connection

    @asynccontextmanager
    async def get_connection(self) -> tp.AsyncGenerator[asyncpg.Connection, tp.Any]:
        if not self._connection_pool:
            raise Exception("Connection pool is not initialized!")

        connection = await self._connection_pool.acquire()
        try:
            yield connection
        finally:
            await self._connection_pool.release(connection)

    async def connect(self) -> None:
        if self._connection_pool is not None:
            return

        self._connection_pool = await asyncpg.create_pool(
            min_size=self._pool_min_size,
            max_size=self._pool_max_size,
            command_timeout=self._timeout,
            user=self.connection.user,
            host=self.connection.host,
            password=self.connection.password,
            database=self.connection.database,
            port=self.connection.port,
        )

    async def close(self) -> None:
        await self._connection_pool.close()
