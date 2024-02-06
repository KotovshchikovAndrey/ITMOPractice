from kink import inject

from domain.repositories.city_point_repository import ICityPointRepository
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection


@inject(alias=ICityPointRepository)
class PostgresCityPointRepository(ICityPointRepository):
    _master_connection: PostgresMasterConnection
    _slave_connection: PostgresSlaveConnection

    def __init__(
        self,
        master_connection: PostgresMasterConnection,
        slave_connection: PostgresSlaveConnection,
    ) -> None:
        self._master_connection = master_connection
        self._slave_connection = slave_connection

    async def test_init(self):
        async with self._slave_connection.get_connection() as connection:
            rows = await connection.fetch("SELECT * FROM public.hash_table;")
            print(rows)
