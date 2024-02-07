import typing as tp
from uuid import UUID

from pydantic import BaseModel

from domain.models.city_point import CityInDb, TagPoints


class GetCitiesResponse(BaseModel):
    cities: tp.List[CityInDb] = []


class GetCityPointsResponse(BaseModel):
    city_pk: UUID
    points: tp.List[TagPoints] = []


class SuccessMessageResponse(BaseModel):
    message: str


class CityCreateResponse(SuccessMessageResponse):
    city_pk: UUID


class PointCreateResponse(SuccessMessageResponse):
    point_pk: UUID
