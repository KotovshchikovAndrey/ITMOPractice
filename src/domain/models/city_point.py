import typing as tp
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, conlist


class CityInDb(BaseModel):
    pk: tp.Annotated[UUID, Field(default_factory=uuid4)]
    name: tp.Annotated[str, Field(min_length=2, max_length=70)]
    description: tp.Annotated[tp.Optional[str], Field(max_length=300, default=None)]
    image_url: tp.Annotated[tp.Optional[str], Field(max_length=255, default=None)]

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    name: tp.Annotated[str, Field(min_length=2, max_length=70)]
    description: tp.Annotated[tp.Optional[str], Field(max_length=300, default=None)]


class BasePoint(BaseModel):
    title: str
    subtitle: str
    description: tp.Annotated[str, Field(default="")]
    image_url: tp.Optional[str] = None
    coordinates: tp.Tuple[int, int]

    class Config:
        from_attributes = True


class PointInDb(BasePoint):
    pk: tp.Annotated[UUID, Field(default_factory=uuid4)]
    city_pk: UUID


class PointCreate(BasePoint):
    city_pk: UUID
    tags: conlist(str, min_length=1)


class PointInFavorite(BasePoint):
    tag_name: str


class TagPoints(BaseModel):
    tag_name: str
    points: tp.List[BasePoint] = []


class BaseFavoritePoint(BaseModel):
    user_pk: UUID
    point_pk: UUID
    created_at: tp.Annotated[datetime, Field(default_factory=datetime.utcnow)]


class FavoritePointInDb(BaseFavoritePoint):
    pk: int

    class Config:
        from_attributes = True


class FavoritePointCreate(BaseFavoritePoint): ...


class TagsCreate(BaseModel):
    tags: conlist(str, min_length=1)
