from kink import di

from infrastructure.config.settings import settings
from infrastructure.database.postgres.dto import PostgresConnectionDTO
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection

# need to inject
from infrastructure.repositories import *


def setup_di_container() -> None:
    di[PostgresSlaveConnection] = PostgresSlaveConnection(
        connections=[
            PostgresConnectionDTO(
                user=settings.postgresql_user,
                host=settings.postgresql_host,
                password=settings.postgresql_password,
                database=settings.postgresql_database,
                port=settings.postgresql_port + 1,
            ),
            PostgresConnectionDTO(
                user=settings.postgresql_user,
                host=settings.postgresql_host,
                password=settings.postgresql_password,
                database=settings.postgresql_database,
                port=settings.postgresql_port + 2,
            ),
        ]
    )

    di[PostgresMasterConnection] = PostgresMasterConnection(
        connection=PostgresConnectionDTO(
            user=settings.postgresql_user,
            host=settings.postgresql_host,
            password=settings.postgresql_password,
            database=settings.postgresql_database,
            port=settings.postgresql_port,
        )
    )
