import typing as tp
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from kink import di

from domain.config.settings import ConstSettings
from domain.models.auth import (
    AuthenticatedUser,
    UserLogin,
    UserLoginConfirm,
    UserRegister,
)
from domain.services.auth.token_auth_service import TokenAuthService
from infrastructure.api.dto import auth_responses as responses
from infrastructure.api.middlewares.authentication import authenticate_current_user

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=responses.UserRegisterResponse,
)
async def register_new_user(
    service: tp.Annotated[TokenAuthService, Depends(lambda: di[TokenAuthService])],
    user: UserRegister,
):
    new_user = await service.register_user(user)
    return {
        "message": "Регистрация прошла успешно! Код для входа в аккаунт отправлен на почту!",
        "user": new_user,
    }


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=responses.UserLoginResponse,
)
async def login_user(
    service: tp.Annotated[TokenAuthService, Depends(lambda: di[TokenAuthService])],
    user: UserLogin,
):
    logined_user = await service.login_user(user)
    return {
        "message": "Код для входа в аккаунт отправлен на почту!",
        "user_pk": logined_user.pk,
    }


@router.post(
    "/confirm-login",
    status_code=status.HTTP_200_OK,
    response_model=responses.UserConfirmLoginResponse,
)
async def confirm_user_login(
    service: tp.Annotated[TokenAuthService, Depends(lambda: di[TokenAuthService])],
    user: UserLoginConfirm,
    response: Response,
):
    logined_user, token = await service.confirm_user_login(user)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=ConstSettings.token_ttl,
    )

    return {
        "message": "Успешный вход в аккаунт!",
        "token": token,
        "user": logined_user,
    }


@router.delete(
    "/logout/{user_pk}",
    status_code=status.HTTP_200_OK,
    response_model=responses.SuccessMessageResponse,
)
async def logout_user(
    service: tp.Annotated[TokenAuthService, Depends(lambda: di[TokenAuthService])],
    current_user: tp.Annotated[AuthenticatedUser, Depends(authenticate_current_user)],
    response: Response,
):
    await service.logout_user(user_pk=current_user.pk, token=current_user.token)
    response.delete_cookie(key="token")

    return {"message": "Успешный выход из аккаунта!"}
