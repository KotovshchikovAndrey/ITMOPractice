import typing as tp
from abc import abstractmethod

from infrastructure.database.postgres.dto import PostgresConnectionDTO
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection


class IPostgresConnectionFactory:
    @abstractmethod
    def create_mester(self) -> PostgresMasterConnection: ...

    @abstractmethod
    def create_slave(self) -> PostgresSlaveConnection: ...


class DevPostgresConnectionFactory(IPostgresConnectionFactory):
    _connection_config: PostgresConnectionDTO

    def __init__(self, connection_config: PostgresConnectionDTO) -> None:
        self._connection_config = connection_config

    def create_mester(self):
        return PostgresMasterConnection(connection=self._connection_config)

    def create_slave(self):
        return PostgresSlaveConnection(connections=[self._connection_config])


class ProdPostgresConnectionFactory(IPostgresConnectionFactory):
    _connection_config: PostgresConnectionDTO
    _slave_replic_count: int

    def __init__(
        self, connection_config: PostgresConnectionDTO, slave_replic_count: int
    ) -> None:
        self._connection_config = connection_config
        self._slave_replic_count = slave_replic_count

    def create_mester(self):
        return PostgresMasterConnection(connection=self._connection_config)

    def create_slave(self):
        connections = []
        for port in range(
            self._connection_config.port + 1,
            self._connection_config.port + self._slave_replic_count + 1,
        ):
            connection_config = self._connection_config.to_dict()
            connection_config["port"] = port
            connections.append(PostgresConnectionDTO(**connection_config))

        return PostgresSlaveConnection(connections=connections)
