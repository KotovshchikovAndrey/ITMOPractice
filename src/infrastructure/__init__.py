from kink import inject

from infrastructure.config.di_container import setup_di_container
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection

setup_di_container()


@inject
async def on_startup(
    master_connection: PostgresMasterConnection,
    slave_connection: PostgresSlaveConnection,
) -> None:
    await master_connection.connect()
    await slave_connection.connect()


@inject
async def on_shutdown(
    master_connection: PostgresMasterConnection,
    slave_connection: PostgresSlaveConnection,
) -> None:
    await master_connection.close()
    await slave_connection.close()
