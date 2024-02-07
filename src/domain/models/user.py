import typing as tp
from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    name: tp.Annotated[str, Field(max_length=70, min_length=2)]
    surname: tp.Annotated[str, Field(max_length=70, min_length=2)]
    email: tp.Annotated[EmailStr, Field(max_length=70)]
    birthday: tp.Optional[date] = None
    created_at: tp.Annotated[datetime, Field(default_factory=datetime.utcnow)]


class UserInDb(BaseUser):
    pk: tp.Annotated[UUID, Field(default_factory=uuid4)]

    class Config:
        from_attributes = True


class UserCreate(BaseUser):
    ...
