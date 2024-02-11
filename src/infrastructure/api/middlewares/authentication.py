import typing as tp
from uuid import UUID

from fastapi import Cookie, Depends
from kink import di

from domain.exceptions.authentication_failed import AuthenticationFailed
from domain.models.auth import AuthenticatedUser
from domain.services.auth.token_auth_service import TokenAuthService


async def authenticate_current_user(
    user_pk: UUID,
    service: tp.Annotated[TokenAuthService, Depends(lambda: di[TokenAuthService])],
    token: tp.Optional[str] = Cookie(default=None),
):
    if token is None:
        raise AuthenticationFailed()

    current_user = await service.authenticate_user(user_pk, token)
    return AuthenticatedUser(pk=current_user.pk, email=current_user.email, token=token)
