from kink import di

from infrastructure.config.settings import settings
from infrastructure.database.postgres.connection_factory import (
    DevPostgresConnectionFactory,
    PostgresConnectionDTO,
    PostgresMasterConnection,
    PostgresSlaveConnection,
    ProdPostgresConnectionFactory,
)

# need to inject
from infrastructure.repositories import *


def setup_di_container() -> None:
    if settings.is_dev:
        _setup_dev_di_container()
        return

    _setup_prod_di_container()


def _setup_dev_di_container() -> None:
    connection_factory = DevPostgresConnectionFactory(
        connection_config=PostgresConnectionDTO(
            user=settings.postgresql_user,
            host=settings.postgresql_host,
            password=settings.postgresql_password,
            database=settings.postgresql_database,
            port=settings.postgresql_port,
        )
    )

    di[PostgresMasterConnection] = connection_factory.create_mester()
    di[PostgresSlaveConnection] = connection_factory.create_slave()


def _setup_prod_di_container() -> None:
    connection_factory = ProdPostgresConnectionFactory(
        slave_replic_count=2,
        connection_config=PostgresConnectionDTO(
            user=settings.postgresql_user,
            host=settings.postgresql_host,
            password=settings.postgresql_password,
            database=settings.postgresql_database,
            port=settings.postgresql_port,
        ),
    )

    di[PostgresMasterConnection] = connection_factory.create_mester()
    di[PostgresSlaveConnection] = connection_factory.create_slave()
