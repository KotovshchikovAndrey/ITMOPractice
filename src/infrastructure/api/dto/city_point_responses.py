import typing as tp
from uuid import UUID

from pydantic import BaseModel

from domain.models.city_point import CityInDb, PointDetail, TagPoints
from infrastructure.api.dto.common import SuccessMessageResponse


class GetCitiesResponse(BaseModel):
    cities: tp.List[CityInDb] = []


class GetCityPointsResponse(BaseModel):
    city: CityInDb
    points: tp.List[TagPoints] = []


class CityCreateResponse(SuccessMessageResponse):
    city_pk: UUID


class PointCreateResponse(SuccessMessageResponse):
    point_pk: UUID


class PointDetailResponse(BaseModel):
    point: PointDetail
