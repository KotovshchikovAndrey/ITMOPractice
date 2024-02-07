import typing as tp
from typing import List
from uuid import UUID
from kink import inject

from domain.models.city_point import CityInDb, PointInDb, PointWithTag
from domain.repositories.city_point_repository import ICityPointRepository
from infrastructure.database.postgres.master_connection import PostgresMasterConnection
from infrastructure.database.postgres.slave_connection import PostgresSlaveConnection


@inject(alias=ICityPointRepository)
class PostgresCityPointRepository(ICityPointRepository):
    _read_connection: PostgresSlaveConnection
    _write_connection: PostgresMasterConnection

    def __init__(
        self,
        read_connection: PostgresSlaveConnection,
        write_connection: PostgresMasterConnection,
    ) -> None:
        self._read_connection = read_connection
        self._write_connection = write_connection

    async def get_cities(self, limit: int, offset: int):
        query = """SELECT * FROM city ORDER BY name LIMIT $1 OFFSET $2;"""
        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, limit, offset)
            return [CityInDb(**dict(row)) for row in rows]

    async def get_city_by_pk(self, city_pk: UUID):
        query = """SELECT * FROM city WHERE pk = $1;"""
        async with self._read_connection.get_connection() as connection:
            row = await connection.fetchrow(query, city_pk)
            if row is not None:
                return CityInDb(**dict(row))

    async def create_city(self, city: CityInDb):
        query = """INSERT INTO city (
                    pk, 
                    name, 
                    description, 
                    image_url) 
                VALUES ($1, $2, $3, $4) RETURNING pk;"""

        async with self._write_connection.get_connection() as connection:
            return await connection.fetchval(query, *city.model_dump().values())

    async def get_city_points_with_tag(self, city_pk: UUID):
        query = """SELECT 
                    p.title, 
                    p.subtitle, 
                    p.description, 
                    p.image_url, 
                    p.coordinates,
                    t.name as tag_name
                FROM point AS p
                    JOIN point_tag AS pt ON pt.point_pk = p.pk
                    JOIN tag AS t ON t.name = pt.tag_name
                WHERE p.city_pk = $1;"""

        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, city_pk)
            return [PointWithTag(**dict(row)) for row in rows]

    async def create_point(self, point: PointInDb):
        query = """INSERT INTO point (
                        title, 
                        subtitle, 
                        description, 
                        image_url, 
                        coordinates,
                        pk,
                        city_pk) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING pk;"""

        async with self._write_connection.get_connection() as connection:
            return await connection.fetchval(query, *point.model_dump().values())

    async def get_all_tag_names(self):
        query = """SELECT name FROM tag;"""
        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query)
            return [dict(row)["name"] for row in rows]

    async def create_tags(self, tags: tp.List[str]):
        query = """INSERT INTO tag VALUES ($1);"""
        async with self._write_connection.get_connection() as connection:
            await connection.executemany(query, [(tag,) for tag in tags])

    async def set_tags_for_point(self, tags: tp.List[str], point_pk: UUID):
        query = """INSERT INTO point_tag (
                    point_pk, 
                    tag_name) 
                VALUES ($1, $2);"""

        async with self._write_connection.get_connection() as connection:
            await connection.executemany(query, [(point_pk, tag) for tag in tags])
