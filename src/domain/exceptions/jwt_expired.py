from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class JwtExpired(ApiException):
    status = ApiExceptionStatus.UNAUTHORIZED
    message = "Токен просрочен!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
