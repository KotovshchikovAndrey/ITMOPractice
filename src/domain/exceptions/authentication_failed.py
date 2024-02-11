from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class AuthenticationFailed(ApiException):
    status = ApiExceptionStatus.UNAUTHORIZED
    message = "Ошибка аутентификации!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
