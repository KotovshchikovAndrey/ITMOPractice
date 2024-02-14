from kink import inject

from infrastructure.config.di_container import setup_di_container
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection
from infrastructure.database.redis.connection import RedisConnection

setup_di_container()


@inject
async def on_startup(
    redis_connection: RedisConnection,
    master_connection: PostgresMasterConnection,
    slave_connection: PostgresSlaveConnection,
) -> None:
    await redis_connection.connect()

    await master_connection.connect()
    await slave_connection.connect()


@inject
async def on_shutdown(
    redis_connection: RedisConnection,
    master_connection: PostgresMasterConnection,
    slave_connection: PostgresSlaveConnection,
) -> None:
    await redis_connection.close()

    await master_connection.close()
    await slave_connection.close()
