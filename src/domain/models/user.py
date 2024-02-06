import typing as tp
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field


class UserInDb(BaseModel):
    pk: UUID
    name: str
    surname: str
    birthday: date
    created_at: tp.Annotated[datetime, Field(default_factory=datetime.utcnow)]

    class Config:
        from_attributes = True
