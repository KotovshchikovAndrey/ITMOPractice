import typing as tp
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from domain.models.user import BaseUser


class UserRegister(BaseModel):
    name: tp.Annotated[str, Field(max_length=70, min_length=2)]
    surname: tp.Annotated[str, Field(max_length=70, min_length=2)]
    email: tp.Annotated[str, EmailStr]


class UserLogin(BaseModel):
    email: tp.Annotated[str, EmailStr]


class UserLoginConfirm(BaseModel):
    user_pk: UUID
    code: str


class AuthenticatedUser(BaseUser):
    token: str
