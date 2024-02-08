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
                user=settings.postgres_user,
                host=settings.postgres_host,
                password=settings.postgres_password,
                database=settings.postgres_database,
            ),
        ]
    )

    di[PostgresMasterConnection] = PostgresMasterConnection(
        connection=PostgresConnectionDTO(
            user=settings.postgres_user,
            host=settings.postgres_host,
            password=settings.postgres_password,
            database=settings.postgres_database,
        )
    )
