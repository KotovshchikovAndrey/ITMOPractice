import asyncio
import typing as tp
from contextlib import asynccontextmanager

import asyncpg

from infrastructure.database.postgres.dto import PostgresConnectionDTO


class PostgresSlaveConnection:
    _pool_min_size: int = 1
    _pool_max_size: int = 3
    _timeout: int = 30

    _current_pool: int = 0
    _connection_pools: tp.List[asyncpg.Pool] = []

    def __init__(self, connections: tp.List[PostgresConnectionDTO]) -> None:
        self.connections = connections

    @asynccontextmanager
    async def get_connection(self) -> asyncpg.Connection:
        if not self._connection_pools:
            raise Exception("Connection pools is empty!")

        pool = self._connection_pools[self._current_pool]
        connection = await pool.acquire()
        try:
            yield connection
        finally:
            await pool.release(connection)
            if self._current_pool < len(self._connection_pools) - 1:
                self._current_pool += 1
            else:
                self._current_pool = 0

    async def connect(self) -> None:
        for connection in self.connections:
            pool = await asyncpg.create_pool(
                min_size=self._pool_min_size,
                max_size=self._pool_max_size,
                command_timeout=self._timeout,
                user=connection.user,
                host=connection.host,
                password=connection.password,
                database=connection.database,
                port=connection.port,
            )

            self._connection_pools.append(pool)

    async def close(self) -> None:
        async with asyncio.TaskGroup() as tg:
            for pool in self._connection_pools:
                tg.create_task(pool.close())
