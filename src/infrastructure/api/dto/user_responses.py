import typing as tp

from pydantic import BaseModel

from domain.models.city_point import TagPoints
from infrastructure.api.dto.common import SuccessMessageResponse


class MyFavoritePointsResponse(BaseModel):
    favorite_points: tp.List[TagPoints] = []
