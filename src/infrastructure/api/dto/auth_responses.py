from uuid import UUID

from pydantic import BaseModel

from domain.models.user import UserCreate, UserInDb
from infrastructure.api.dto.common import SuccessMessageResponse


class UserRegisterResponse(SuccessMessageResponse):
    user: UserCreate


class UserLoginResponse(SuccessMessageResponse):
    user_pk: UUID


class UserConfirmLoginResponse(UserRegisterResponse):
    token: str
