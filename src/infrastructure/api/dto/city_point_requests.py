import typing as tp
from uuid import UUID

from fastapi import Form

from domain.models.city_point import CityCreate, PointCreate


class CityCreateRequest:
    @staticmethod
    def as_form(
        name: tp.Annotated[str, Form()],
        description: tp.Annotated[tp.Optional[str], Form()] = None,
    ) -> CityCreate:
        return CityCreate(name=name, description=description)


class PointCreateRequest:
    @staticmethod
    def as_form(
        title: tp.Annotated[str, Form()],
        coordinates: tp.Annotated[tp.Tuple[float, float], Form()],
        subtitle: tp.Annotated[str, Form()],
        description: tp.Annotated[str, Form()],
        city_pk: tp.Annotated[UUID, Form()],
        tags: tp.Annotated[tp.Set[str], Form()],
    ) -> PointCreate:
        print(tags)
        return PointCreate(
            title=title,
            coordinates=coordinates,
            subtitle=subtitle,
            description=description,
            city_pk=city_pk,
            tags=tags,
        )
