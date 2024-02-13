import typing as tp
from typing import List
from uuid import UUID

from kink import inject

from domain.models.city_point import (
    BasePoint,
    CityInDb,
    PointDetail,
    PointInDb,
    PointWithTag,
    Tag,
)
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
                    p.pk, 
                    p.title, 
                    p.coordinates::geometry::point,
                    t.pk AS tag_pk,
                    t.name AS tag_name
                FROM point AS p
                    JOIN point_tag AS pt ON pt.point_pk = p.pk
                    JOIN tag AS t ON t.pk = pt.tag_pk
                WHERE p.city_pk = $1;"""

        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, city_pk)
            result = []
            for row in rows:
                row_data = dict(row)
                tag = Tag(pk=row_data.pop("tag_pk"), name=row_data.pop("tag_name"))
                result.append(PointWithTag(**row_data, tag=tag))

            return result

    async def get_point_by_pk(self, point_pk: UUID):
        query = """SELECT
                    pk, 
                    title,
                    subtitle,
                    description,
                    image_url,
                    coordinates::geometry::point
                FROM point WHERE pk = $1;"""

        async with self._read_connection.get_connection() as connection:
            row = await connection.fetchrow(query, point_pk)
            if row is not None:
                return PointDetail(**dict(row))

    async def get_point_by_coordinates(self, coordinates: tp.Tuple[float, float]):
        query = """SELECT
                    pk, 
                    title, 
                    coordinates::geometry::point
                FROM point WHERE ST_X(coordinates::geometry) = $1 
                    AND ST_Y(coordinates::geometry) = $2;"""

        async with self._read_connection.get_connection() as connection:
            row = await connection.fetchrow(query, *coordinates)
            if row is not None:
                return BasePoint(**dict(row))

    async def create_point(self, point: PointInDb):
        query = """INSERT INTO point (
                    pk,
                    title, 
                    subtitle, 
                    description, 
                    image_url, 
                    city_pk,
                    coordinates) 
                VALUES ($1, $2, $3, $4, $5, $6, ST_POINT($7, $8)) RETURNING pk;"""

        async with self._write_connection.get_connection() as connection:
            return await connection.fetchval(
                query,
                *point.model_dump(exclude=("coordinates",)).values(),
                *point.coordinates
            )

    async def favorite_point_exists(self, user_pk: UUID, point_pk: UUID):
        query = """SELECT pk FROM favorite_point 
                        WHERE user_pk = $1 AND point_pk = $2;"""

        async with self._read_connection.get_connection() as connection:
            pk = await connection.fetchval(query, user_pk, point_pk)
            return pk is not None

    async def get_favorite_points_by_city(self, user_pk: UUID, city_pk: UUID):
        query = """SELECT
                    p.pk, 
                    p.title, 
                    p.coordinates::geometry::point
                FROM point AS p
                    JOIN favorite_point AS fp ON fp.point_pk = p.pk
                WHERE fp.user_pk = $1 AND p.city_pk = $2;"""

        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, user_pk, city_pk)
            return [BasePoint(**dict(row)) for row in rows]

    async def get_favorite_points_with_tag(self, user_pk: UUID):
        query = """SELECT
                    p.pk, 
                    p.title, 
                    p.coordinates::geometry::point,
                    t.pk AS tag_pk,
                    t.name AS tag_name
                FROM point AS p
                    JOIN favorite_point AS fp ON fp.point_pk = p.pk
                    JOIN point_tag AS pt ON pt.point_pk = p.pk
                    JOIN tag AS t ON t.pk = pt.tag_pk
                WHERE fp.user_pk = $1;"""

        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, user_pk)
            result = []
            for row in rows:
                row_data = dict(row)
                tag = Tag(pk=row_data.pop("tag_pk"), name=row_data.pop("tag_name"))
                result.append(PointWithTag(**row_data, tag=tag))

            return result

    async def set_favorite_point(self, user_pk: UUID, point_pk: UUID):
        query = """INSERT INTO favorite_point (
                    user_pk,
                    point_pk)
                VALUES ($1, $2);"""

        async with self._write_connection.get_connection() as connection:
            await connection.execute(query, user_pk, point_pk)

    async def delete_favorite_point(self, user_pk: UUID, point_pk: UUID):
        query = """DELETE FROM favorite_point 
                    WHERE user_pk = $1 AND point_pk = $2;"""

        async with self._write_connection.get_connection() as connection:
            await connection.execute(query, user_pk, point_pk)

    async def get_all_tag_names(self):
        query = """SELECT name FROM tag;"""
        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query)
            return [dict(row)["name"] for row in rows]

    async def get_tags_by_names(self, tag_names: tp.Set[str]):
        query = """SELECT pk, name FROM tag WHERE name = ANY($1::text[]);"""
        async with self._read_connection.get_connection() as connection:
            rows = await connection.fetch(query, tag_names)
            return [Tag(**dict(row)) for row in rows]

    async def create_tags(self, tags: tp.Iterable[Tag]):
        query = """INSERT INTO tag VALUES ($1, $2);"""
        async with self._write_connection.get_connection() as connection:
            await connection.executemany(query, [(tag.pk, tag.name) for tag in tags])

    async def set_tags_for_point(self, tags: tp.Iterable[Tag], point_pk: UUID):
        query = """INSERT INTO point_tag (
                    point_pk, 
                    tag_pk) 
                VALUES ($1, $2);"""

        async with self._write_connection.get_connection() as connection:
            await connection.executemany(query, [(point_pk, tag.pk) for tag in tags])
