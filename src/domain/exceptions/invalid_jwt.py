from domain.exceptions.api_exception import ApiException, ApiExceptionStatus


class InvalidJwt(ApiException):
    status = ApiExceptionStatus.UNAUTHORIZED
    message = "Невалидный токен!"

    def __init__(self) -> None:
        super().__init__(status=self.status, message=self.message)
