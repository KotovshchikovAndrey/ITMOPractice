import asyncio
import hashlib
import random
import typing as tp
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt as jwt_service
from kink import inject

from domain.config.settings import ConstSettings
from domain.exceptions.authentication_failed import AuthenticationFailed
from domain.exceptions.invalid_auth_code import InvalidAuthCode
from domain.exceptions.invalid_jwt import InvalidJwt
from domain.exceptions.jwt_expired import JwtExpired
from domain.exceptions.user_not_found import UserNotFound
from domain.models.auth import UserLogin, UserLoginConfirm, UserRegister
from domain.models.user import UserCreate, UserEmailCodeSend
from domain.repositories.auth_code_repository import IAuthCodeRepository
from domain.repositories.jwt_repository import IJwtRepository
from domain.services.mail_sender_service import MailSenderService
from domain.services.user_service import UserService


@inject
class JwtAuthService:
    _user_service: UserService
    _mail_sender_service: MailSenderService
    _auth_code_storage: IAuthCodeRepository
    _repository: IJwtRepository
    _secret_key: str

    def __init__(
        self,
        repository: IJwtRepository,
        user_service: UserService,
        mail_sender_service: MailSenderService,
        auth_code_storage: IAuthCodeRepository,
        secret_key: str,
    ) -> None:
        self._user_service = user_service
        self._mail_sender_service = mail_sender_service
        self._repository = repository
        self._auth_code_storage = auth_code_storage
        self._secret_key = secret_key

    async def authenticate_user(self, token: str, finger_print: str):
        user_pk = self._validate_user_jwt(jwt=token)
        user = await self._user_service.get_user_by_pk(user_pk)
        if user is None:
            raise AuthenticationFailed()

        jwt_hash = self._get_jwt_hash(token, finger_print)
        jwt = await self._repository.get_jwt_by_hash(jwt_hash)
        if jwt is None:
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

        return user_in_db

    async def confirm_user_login(self, user: UserLoginConfirm, finger_print: str):
        """Return logined user and access token"""

        user_in_db = await self._user_service.get_user_by_pk(user.user_pk)
        if user_in_db is None:
            raise UserNotFound()

        login_code = await self._auth_code_storage.get_user_login_code(user_in_db.pk)
        if login_code != user.code:
            raise InvalidAuthCode()

        jwt = self._generate_user_jwt(user_in_db.pk)
        jwt_hash = self._get_jwt_hash(jwt, finger_print)

        async with asyncio.TaskGroup() as tg:
            tg.create_task(
                self._repository.set_jwt(jwt_hash, jwt, ConstSettings.token_ttl)
            )

            tg.create_task(
                self._auth_code_storage.delete_user_login_code(user_in_db.pk)
            )

        return user_in_db, jwt

    async def logout_user(self, jwt: str):
        await self._repository.delete_jwt(jwt)

    async def _send_login_code_by_email(self, user: UserEmailCodeSend) -> None:
        login_code = await self._auth_code_storage.get_user_login_code(user.pk)
        if login_code is not None:
            return

        login_code = self._generate_code()
        await self._auth_code_storage.set_user_login_code(
            user_pk=user.pk,
            code=login_code,
            ttl=ConstSettings.login_code_ttl,
        )

        await self._mail_sender_service.send_login_code_by_email(
            code=login_code,
            email=user.email,
        )

    def _generate_code(self, length: int = 6) -> str:
        code = [str(random.randint(1, 9)) for _ in range(length)]
        return "".join(code)

    def _generate_user_jwt(self, user_pk: str) -> str:
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=ConstSettings.token_ttl)
        return jwt_service.encode(
            payload={"user_pk": str(user_pk), "exp": exp},
            key=self._secret_key,
            algorithm="HS256",
        )

    def _validate_user_jwt(self, jwt: str) -> UUID:
        """Return user primary key"""

        try:
            payload = jwt_service.decode(jwt, self._secret_key, algorithms=["HS256"])
            return UUID(payload["user_pk"])
        except jwt_service.ExpiredSignatureError:
            raise JwtExpired()
        except jwt_service.InvalidTokenError:
            raise InvalidJwt()

    def _get_jwt_hash(self, jwt: str, finger_print: str) -> str:
        return hashlib.sha3_256((jwt + finger_print).encode()).hexdigest()
