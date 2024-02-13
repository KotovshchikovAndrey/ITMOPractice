import typing as tp

from fastapi import Cookie, Depends, Header
from kink import di

from domain.exceptions.authentication_failed import AuthenticationFailed
from domain.models.auth import AuthenticatedUser
from domain.services.auth.jwt_auth_service import JwtAuthService


async def authenticate_current_user(
    service: tp.Annotated[JwtAuthService, Depends(lambda: di[JwtAuthService])],
    token: tp.Optional[str] = Cookie(default=None),
    finger_print: tp.Optional[str] = Header(None),
):
    if (token is None) or (finger_print is None):
        raise AuthenticationFailed()

    current_user = await service.authenticate_user(token, finger_print)
    return AuthenticatedUser(pk=current_user.pk, email=current_user.email, token=token)
