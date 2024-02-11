import asyncio
import hashlib
import random
import typing as tp
from datetime import datetime
from uuid import UUID

from kink import inject

from domain.config.settings import ConstSettings
from domain.exceptions.authentication_failed import AuthenticationFailed
from domain.exceptions.invalid_auth_code import InvalidAuthCode
from domain.exceptions.user_not_found import UserNotFound
from domain.models.auth import UserLogin, UserLoginConfirm, UserRegister
from domain.models.user import UserCreate, UserEmailCodeSend, UserInDb
from domain.repositories.auth_repository import IAuthRepository
from domain.services.mail_sender_service import MailSenderService
from domain.services.user_service import UserService


@inject
class TokenAuthService:
    _user_service: UserService
    _mail_sender_service: MailSenderService
    _repository: IAuthRepository

    def __init__(
        self,
        user_service: UserService,
        mail_sender_service: MailSenderService,
        repository: IAuthRepository,
    ) -> None:
        self._user_service = user_service
        self._mail_sender_service = mail_sender_service
        self._repository = repository

    async def authenticate_user(self, user_pk: UUID, token: str) -> UserInDb:
        user = await self._user_service.get_user_by_pk(user_pk)
        if user is None:
            raise AuthenticationFailed()

        if not await self._repository.is_user_token_exists(user_pk, token):
            raise AuthenticationFailed()

        return user

    async def register_user(self, user: UserRegister):
        user_create = UserCreate(**user.model_dump())
        await self._user_service.create_user(user_create)

        user_email_code = UserEmailCodeSend.model_validate(user_create)
        asyncio.create_task(self._send_login_code_by_email(user_email_code))

        return user_create

    async def login_user(self, user: UserLogin):
        user_in_db = await self._user_service.get_user_by_email(user.email)
        if user_in_db is None:
            raise UserNotFound()

        user_email_code = UserEmailCodeSend.model_validate(user_in_db)
        asyncio.create_task(self._send_login_code_by_email(user_email_code))
        asyncio.create_task(self._repository.delete_expired_user_tokens(user_in_db.pk))

        return user_in_db

    async def confirm_user_login(self, user: UserLoginConfirm):
        """Return logined user and token"""

        user_in_db = await self._user_service.get_user_by_pk(user_pk=user.user_pk)
        if user_in_db is None:
            raise UserNotFound()

        login_code = await self._repository.get_user_login_code(user_pk=user_in_db.pk)
        if login_code != user.code:
            raise InvalidAuthCode()

        token = self._generate_user_token(user_in_db.pk)
        await self._repository.set_user_token(
            user_pk=user_in_db.pk,
            token=token,
            ttl=ConstSettings.token_ttl,
        )

        await self._repository.delete_user_login_code(user_pk=user_in_db.pk)
        return user_in_db, token

    async def logout_user(self, user_pk: UUID, token: str):
        await self._repository.delete_user_token(user_pk, token)

    async def _send_login_code_by_email(self, user: UserEmailCodeSend) -> None:
        login_code = await self._repository.get_user_login_code(user.pk)
        if login_code is not None:
            return

        login_code = self._generate_code()
        await self._repository.set_user_login_code(
            user_pk=user.pk,
            code=login_code,
            ttl=ConstSettings.login_code_ttl,  # 30 minutes
        )

        await self._mail_sender_service.send_login_code_by_email(
            code=login_code,
            email=user.email,
        )

    def _generate_code(self, length: int = 6) -> str:
        code = [str(random.randint(1, 9)) for _ in range(length)]
        return "".join(code)

    def _generate_user_token(self, user_pk: UUID) -> str:
        current_timestamp = datetime.utcnow().timestamp()
        return hashlib.sha3_256(f"{user_pk}{current_timestamp}".encode()).hexdigest()
