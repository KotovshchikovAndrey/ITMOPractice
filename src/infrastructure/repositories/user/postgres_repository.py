from uuid import UUID

from kink import inject

from domain.models.user import UserInDb
from domain.repositories.user_repository import IUserRepository
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection


@inject(alias=IUserRepository)
class PostgresUserRepository(IUserRepository):
    _read_connection: PostgresSlaveConnection
    _write_connection: PostgresMasterConnection

    def __init__(
        self,
        read_connection: PostgresSlaveConnection,
        write_connection: PostgresMasterConnection,
    ) -> None:
        self._read_connection = read_connection
        self._write_connection = write_connection

    async def get_user_by_pk(self, user_pk: UUID):
        query = """SELECT 
                    pk,
                    name,
                    surname,
                    email,
                    birthday,
                    created_at
                FROM user WHERE pk = $1;"""

        async with self._read_connection.get_connection() as connection:
            row = await connection.fetchrow(query, user_pk)
            if row is not None:
                return UserInDb(**dict(row))

    async def get_user_by_email(self, email: str):
        query = """SELECT 
                    pk,
                    name,
                    surname,
                    email,
                    birthday,
                    created_at
                FROM user WHERE email = $1;"""

        async with self._read_connection.get_connection() as connection:
            row = await connection.fetchrow(query, email)
            if row is not None:
                return UserInDb(**dict(row))

    async def create_user(self, user: UserInDb) -> UUID:
        query = """INSERT INTO user (
                    name,
                    surname,
                    email,
                    birthday,
                    created_at,
                    pk)
                VALUES ($1, $2, $3, $4, $5) RETURNING pk;"""

        async with self._write_connection.get_connection() as connection:
            return await connection.fetchval(query, *user.model_dump().values())
