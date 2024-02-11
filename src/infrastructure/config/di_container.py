from kink import di

from domain.services.mail_sender_service import MailSenderConfigDTO, MailSenderService
from infrastructure.config.settings import settings
from infrastructure.database.postgres.connection_factory import (
    DevPostgresConnectionFactory,
    PostgresConnectionDTO,
    PostgresMasterConnection,
    PostgresSlaveConnection,
    ProdPostgresConnectionFactory,
)
from infrastructure.database.redis.connection import RedisConnection, RedisConnectionDTO

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

    di[RedisConnection] = RedisConnection(
        connection_config=RedisConnectionDTO(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
        )
    )

    di[MailSenderService] = MailSenderService(
        smtp_config=MailSenderConfigDTO(
            sender=settings.sender,
            smtp_host=settings.smtp_host,
            smtp_port=settings.smtp_port,
            smtp_user=settings.smtp_user,
            smtp_password=settings.smtp_password,
        )
    )


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
