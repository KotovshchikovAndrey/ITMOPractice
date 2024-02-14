import typing as tp
from uuid import UUID

from pydantic import BaseModel, field_serializer

from domain.models.city_point import BasePoint, CityInDb, PointDetail, TagPoints
from infrastructure.api.dto.common import SuccessMessageResponse


class GetCitiesResponse(BaseModel):
    cities: tp.List[CityInDb] = []


class PointCoordinatesResponse(BaseModel):
    latitude: float
    longitude: float


class BasePointResponse(BasePoint):
    coordinates: PointCoordinatesResponse


class TagPointsResponse(TagPoints):
    @field_serializer("points", when_used="json")
    def serialize_coordinates(points: tp.List[BasePoint]):
        for index, point in enumerate(points):
            latitude, longitude = point.coordinates
            points[index] = BasePointResponse(
                pk=point.pk,
                title=point.title,
                coordinates=PointCoordinatesResponse(
                    latitude=latitude,
                    longitude=longitude,
                ),
            )

        return points


class GetCityPointsResponse(BaseModel):
    city: CityInDb
    points: tp.List[TagPointsResponse] = []


class CityCreateResponse(SuccessMessageResponse):
    city_pk: UUID


class PointCreateResponse(SuccessMessageResponse):
    point_pk: UUID


class PointDetailResponse(BaseModel):
    point: PointDetail
