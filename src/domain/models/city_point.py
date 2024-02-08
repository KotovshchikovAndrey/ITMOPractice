import typing as tp
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, conlist


class CityInDb(BaseModel):
    pk: tp.Annotated[UUID, Field(default_factory=uuid4)]
    name: tp.Annotated[str, Field(min_length=2, max_length=70)]
    description: tp.Annotated[tp.Optional[str], Field(max_length=300, default=None)]
    image_url: tp.Annotated[tp.Optional[str], Field(max_length=255, default=None)]

    class Config:
        from_attributes = True

    def set_image_url(self, image_url: str) -> None:
        self.image_url = image_url


class CityCreate(BaseModel):
    name: tp.Annotated[str, Field(min_length=2, max_length=70)]
    description: tp.Annotated[tp.Optional[str], Field(max_length=300, default=None)]


class BasePoint(BaseModel):
    pk: tp.Annotated[UUID, Field(default_factory=uuid4)]
    title: str
    coordinates: tp.Tuple[float, float]

    class Config:
        from_attributes = True


class PointInDb(BasePoint):
    subtitle: str
    description: tp.Annotated[str, Field(default="")]
    image_url: tp.Optional[str] = None
    city_pk: UUID

    def set_image_url(self, image_url: str) -> None:
        self.image_url = image_url


class PointDetail(BasePoint):
    subtitle: str
    description: tp.Annotated[str, Field(default="")]
    image_url: tp.Optional[str] = None


class PointCreate(PointDetail):
    city_pk: UUID
    tags: tp.Annotated[tp.Set[str], conlist(str, min_length=1)]


class PointWithTag(BasePoint):
    tag_name: str


class TagPoints(BaseModel):
    tag_name: str
    points: tp.List[BasePoint] = []


class BaseCityPointsCache(BaseModel):
    city_pk: UUID
    points: tp.List[TagPoints] = []

    class Config:
        from_attributes = True


class CityPointsCache(BaseCityPointsCache):
    ttl: tp.Annotated[int, Field(default=60)]  # 1 minute


class TagsCreate(BaseModel):
    tags: conlist(str, min_length=1)
